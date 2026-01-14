import time
import secrets
import hashlib
import base64
import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from aiocache import cached, caches
from jose import jwt
from datetime import datetime, timedelta

from .ton_authorization import verify_ton_proof


class TonAddressData(BaseModel):
    address: str
    chain: str
    publicKey: str
    walletStateInit: str


class TonProofDomain(BaseModel):
    lengthBytes: int
    value: str


class TonProofData(BaseModel):
    domain: TonProofDomain
    payload: str
    signature: str
    timestamp: int


class TonProof(BaseModel):
    proof: TonProofData


class CheckProofRequest(BaseModel):
    public_key: str
    ton_addr: TonAddressData
    ton_proof: TonProof


class TokenResponseModel(BaseModel):
    token: str


class NonceResponse(BaseModel):
    nonce: str


class JWKSResponse(BaseModel):
    keys: list


class Web3TonRouter(APIRouter):
    """
    Router for Web3 TON authentication endpoints.
    Provides JWKS, nonce generation, and proof verification.
    """

    def __init__(self, 
                 jwt_secret: str,
                 jwt_algorithm: str = "HS256",
                 jwt_expiration_minutes: int = 60,
                 nonce_ttl_seconds: int = 300,
                 nonce_secret: Optional[str] = None):
        super().__init__(tags=['Web3 TON'])
        
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expiration_minutes = jwt_expiration_minutes
        self.nonce_ttl_seconds = nonce_ttl_seconds
        # Use provided nonce_secret or derive from jwt_secret for backward compatibility
        self.nonce_secret = nonce_secret or hashlib.sha256(jwt_secret.encode()).hexdigest()
        
        self._setup_routes()

    def _setup_routes(self):
        """Setup all Web3 TON authentication routes"""
        
        @self.get('/.well-known/jwks.json',
                  summary='Get JWKS public keys',
                  response_model=JWKSResponse,
                  tags=["Web3 TON"])
        async def get_jwks():
            """
            Returns JSON Web Key Set (JWKS) for JWT validation.
            Currently returns empty keys array as we use symmetric signing.
            """
            return JWKSResponse(keys=[])

        @self.get('/web3/nonce',
                  summary='Generate nonce for public_key',
                  response_model=NonceResponse,
                  tags=["Web3 TON"])
        async def get_nonce(public_key: str):
            """
            Generates a time-based one-time nonce for a specific public_key
            The nonce is cached per public_key and expires after nonce_ttl_seconds.
            
            Args:
                public_key: Generated nonve by client
            
            Returns:
                NonceResponse with the generated nonce
            """
            return NonceResponse(nonce=await self._generate_nonce(public_key))

        @self.post('/web3/ton/check-proof',
                   summary='Verify TON proof and get JWT token',
                   response_model=TokenResponseModel,
                   tags=["Web3 TON"])
        async def check_proof(request: CheckProofRequest):
            """
            Verifies a TON Connect proof and returns a JWT token.
            
            The JWT token payload contains:
            - address: TON wallet address
            - iat: issued at timestamp
            - exp: expiration timestamp
            
            Args:
                request: CheckProofRequest containing ton_addr and ton_proof
            
            Returns:
                TokenResponseModel with the JWT token
            
            Raises:
                HTTPException: 400 if proof verification fails
            """
            return await self._verify_and_generate_token(request)

    @cached(
        key_builder=lambda f, self, public_key: f"web3:nonce:{public_key}",
        ttl=300,  # 5 minutes
        alias="default"
    )
    async def _generate_nonce(self, public_key: str) -> str:
        """
        Generates a cryptographically secure nonce for a public_key.
        Uses server secret, timestamp, public_key address, and random bytes.
        The nonce is hard to replicate without the server secret.
        The nonce is cached per public_key address.
        
        Args:
            public_key: The TON public_key address
        
        Returns:
            A cryptographically secure nonce string
        """
        # Generate secure nonce using server secret, timestamp, public_key, and random data
        timestamp = int(time.time())
        
        # Use server secret to make nonce generation hard to replicate
        # Combine: server_secret + public_key + time_window + random
        time_window = timestamp // self.nonce_ttl_seconds
        secret_material = f"{self.nonce_secret}:{public_key}:{time_window}"
        secret_hash = hashlib.sha256(secret_material.encode()).digest()
        
        # Add random component for uniqueness (prevents collisions)
        random_bytes = secrets.token_bytes(16)
        
        # Combine server-secret-derived hash with random bytes
        nonce_material = secret_hash + random_bytes + timestamp.to_bytes(8, 'big')
        nonce_hash = hashlib.sha256(nonce_material).digest()
        
        # Return base64url-encoded nonce (URL-safe, no padding)
        nonce = base64.urlsafe_b64encode(nonce_hash).decode('utf-8').rstrip('=')
        
        return nonce

    async def _verify_and_generate_token(self, request: CheckProofRequest) -> TokenResponseModel:
        """
        Verifies the TON proof and generates a JWT token.
        
        Args:
            request: CheckProofRequest containing proof data
        
        Returns:
            TokenResponseModel with JWT token
        
        Raises:
            HTTPException: 400 if verification fails
        """
        # Get cached nonce for this public_key
        expected_payload = await self._get_cached_nonce(request.public_key)
        
        if not expected_payload:
            raise HTTPException(
                status_code=400,
                detail="NOT_FOUND"
            )
        
        # Verify the TON proof
        try:
            verify_ton_proof(
                address_raw=request.ton_addr.address,
                public_key_hex=request.ton_addr.publicKey,
                domain_value=request.ton_proof.proof.domain.value,
                domain_length_bytes=request.ton_proof.proof.domain.lengthBytes,
                timestamp=request.ton_proof.proof.timestamp,
                payload=request.ton_proof.proof.payload,
                signature_b64=request.ton_proof.proof.signature,
                expected_payload=expected_payload,
                wallet_state_init_b64=request.ton_addr.walletStateInit,
                max_skew_seconds=self.nonce_ttl_seconds,
            )
        except AssertionError as e:
            raise HTTPException(status_code=400, detail=f"Proof verification failed: {str(e)}")
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Unexpected error during verification: {str(e)}")
        
        # Generate JWT token with minimal payload (only claims and address)
        now = datetime.utcnow()
        exp = now + timedelta(minutes=self.jwt_expiration_minutes)
        
        payload = {
            "address": request.ton_addr.address,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        
        return TokenResponseModel(token=token)

    async def _get_cached_nonce(self, wallet: str) -> Optional[str]:
        """
        Retrieves cached nonce for a wallet address.
        
        Args:
            wallet: The TON wallet address
        
        Returns:
            The cached nonce or None if not found
        """
        cache = caches.get('default')
        cache_key = f"web3:nonce:{wallet}"
        nonce = await cache.get(cache_key)
        return nonce

