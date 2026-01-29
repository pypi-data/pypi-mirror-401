"""
Median Blockchain Python SDK

This SDK provides Python bindings for the Median blockchain APIs,
using mospy-wallet for proper Protobuf transaction signing.
"""

__version__ = "1.7.0"
__author__ = "Median Team"
__email__ = "contact@median.network"
__license__ = "Apache-2.0"

import json
import time
import requests
import hashlib
import base64
import math
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from mospy import Account, Transaction
from mospy.clients import HTTPClient


from google.protobuf.message import Message as ProtoMessage
from google.protobuf.any_pb2 import Any as AnyPb
try:
    import cosmospy_protobuf.cosmos.feegrant.v1beta1.tx_pb2 as feegrant_tx
    import cosmospy_protobuf.cosmos.feegrant.v1beta1.feegrant_pb2 as feegrant_pb
except ImportError:
    # Handle case where these specific modules might not be available in all environments
    feegrant_tx = None
    feegrant_pb = None

# Monkey patch for protobuf > 4.x compatibility with mospy
import google.protobuf.message_factory
if not hasattr(google.protobuf.message_factory.MessageFactory, 'GetPrototype'):
    def GetPrototype(self, descriptor):
        return google.protobuf.message_factory.GetMessageClass(descriptor)
    google.protobuf.message_factory.MessageFactory.GetPrototype = GetPrototype


class MedianSDKError(Exception):
    """SDK exception for Median-specific errors."""
    pass


@dataclass
class Coin:
    """Represents a coin amount with denomination"""
    denom: str
    amount: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "denom": self.denom,
            "amount": self.amount
        }


class MedianSDK:
    """
    Python SDK for interacting with the Median blockchain.
    """

    def __init__(
        self,
        api_url: str = "http://localhost:1317",
        chain_id: str = "median",
        timeout: int = 30,
        default_gas: int = 100000,  # Empirically tested: standard tx takes ~92k gas
        default_fee_denom: str = "stake",
        gas_price: float = 0.025,  # Default gas price (fee per unit gas)
        gas_adjustment: float = 1.5  # Gas multiplier for safety margin
    ):
        self.api_url = api_url.rstrip('/')
        self.chain_id = chain_id
        self.timeout = timeout
        self.default_gas = default_gas
        self.default_fee_denom = default_fee_denom
        self.gas_price = gas_price
        self.gas_adjustment = gas_adjustment
        self.session = requests.Session()
        self._client = HTTPClient(api=self.api_url) # Mospy client

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        raise_on_error: bool = True
    ) -> Dict[str, Any]:
        url = f"{self.api_url}{endpoint}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            if response.status_code >= 400 and raise_on_error:
                try:
                    error_detail = response.json()
                except:
                    error_detail = {"error": response.text}
                raise MedianSDKError(f"HTTP {response.status_code}: {error_detail}")
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            if raise_on_error:
                raise
            return {"error": str(e)}

    # ==================== Account Management ====================

    def create_account(
        self,
        creator_address: str,
        new_account_address: str,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "creator": creator_address,
            "new_account_address": new_account_address
        }
        return self._broadcast_tx(
            "/median.median.MsgCreateAccount", msg, creator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def get_account(self, address: str) -> Dict[str, Any]:
        endpoint = f"/cosmos/auth/v1beta1/accounts/{address}"
        return self._make_request("GET", endpoint)

    def get_account_balance(self, address: str) -> List[Coin]:
        endpoint = f"/cosmos/bank/v1beta1/balances/{address}"
        response = self._make_request("GET", endpoint)
        balances = response.get("balances", [])
        return [Coin(denom=b["denom"], amount=b["amount"]) for b in balances]

    # ==================== Coin Management ====================

    def mint_coins(
        self,
        authority_address: str,
        recipient_address: str,
        amount: List[Coin],
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "authority": authority_address,
            "recipient": recipient_address,
            "amount": [coin.to_dict() for coin in amount]
        }
        return self._broadcast_tx(
            "/median.median.MsgMintCoins", msg, authority_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def burn_coins(
        self,
        authority_address: str,
        amount: List[Coin],
        from_address: str = "",
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "authority": authority_address,
            "from": from_address,
            "amount": [coin.to_dict() for coin in amount]
        }
        return self._broadcast_tx(
            "/median.median.MsgBurnCoins", msg, authority_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def transfer_coins(
        self,
        from_address: str,
        to_address: str,
        amount: List[Coin],
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        从指定账户转移代币到目标账户

        参数：
            from_address: 发送方地址
            to_address: 接收方地址
            amount: 代币金额列表
            private_key: 发送方私钥
            wait_confirm: 是否等待交易确认
            fee_granter: 代付手续费的地址（可选）

        返回：
            交易结果字典
        """
        msg = {
            "from_address": from_address,
            "to_address": to_address,
            "amount": [coin.to_dict() for coin in amount]
        }
        return self._broadcast_tx("/cosmos.bank.v1beta1.MsgSend", msg, from_address, private_key, wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas)

    # ==================== Task Management ====================

    def create_task(
        self,
        creator_address: str,
        task_id: str,
        description: str,
        input_data: str,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "creator": creator_address,
            "task_id": task_id,
            "description": description,
            "input_data": input_data
        }
        return self._broadcast_tx(
            "/median.median.MsgCreateTask", msg, creator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def commit_result(
        self,
        validator_address: str,
        task_id: str,
        result_hash: str,
        nonce: Optional[int] = None,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "validator": validator_address,
            "task_id": task_id,
            "result_hash": result_hash,
            "nonce": str(nonce if nonce is not None else 0)
        }
        return self._broadcast_tx(
            "/median.median.MsgCommitResult", msg, validator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def reveal_result(
        self,
        validator_address: str,
        task_id: str,
        result: Union[int, float, str],
        nonce: Union[int, str],
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        msg = {
            "validator": validator_address,
            "task_id": task_id,
            "result": str(result),
            "nonce": str(nonce)
        }
        return self._broadcast_tx(
            "/median.median.MsgRevealResult", msg, validator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    # ==================== Query Methods ====================

    def get_task(self, task_id: str) -> Dict[str, Any]:
        endpoint = f"/median/median/task/{task_id}"
        return self._make_request("GET", endpoint)

    def get_consensus_result(self, task_id: str) -> Dict[str, Any]:
        endpoint = f"/median/median/consensus/{task_id}"
        return self._make_request("GET", endpoint)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        endpoint = "/median/median/tasks"
        response = self._make_request("GET", endpoint, raise_on_error=False)
        return response.get("tasks", [])

    def list_commitments(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Query all commitments, optionally filter by task_id"""
        response = self._make_request("GET", "/median/median/commitment", raise_on_error=False)
        if task_id and "commitment" in response:
            response["commitment"] = [c for c in response["commitment"] if c.get("task_id") == task_id]
        return response

    def list_reveals(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Query all reveals, optionally filter by task_id"""
        response = self._make_request("GET", "/median/median/reveal", raise_on_error=False)
        if task_id and "reveal" in response:
            response["reveal"] = [r for r in response["reveal"] if r.get("task_id") == task_id]
        return response

    def list_consensus_results(self) -> Dict[str, Any]:
        """Query all consensus results"""
        return self._make_request("GET", "/median/median/consensus_result", raise_on_error=False)

    # ==================== Blockchain Info ====================

    def get_node_info(self) -> Dict[str, Any]:
        endpoint = "/cosmos/base/tendermint/v1beta1/node_info"
        return self._make_request("GET", endpoint)

    def get_current_height(self) -> int:
        """Query current block height"""
        endpoint = "/cosmos/base/tendermint/v1beta1/blocks/latest"
        result = self._make_request("GET", endpoint, raise_on_error=False)
        return int(result.get("block", {}).get("header", {}).get("height", "0"))

    def get_supply(self, denom: Optional[str] = None) -> Dict[str, Any]:
        endpoint = f"/cosmos/bank/v1beta1/supply/{denom}" if denom else "/cosmos/bank/v1beta1/supply"
        return self._make_request("GET", endpoint)

    # ==================== Staking Methods ====================

    def delegate_tokens(
        self,
        delegator_address: str,
        validator_address: str,
        amount: List[Coin],
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        质押代币给验证者

        参数：
            delegator_address: 质押者地址
            validator_address: 验证者地址
            amount: 代币金额列表（通常为单个代币）
            private_key: 质押者私钥
            wait_confirm: 是否等待交易确认
            fee_granter: 代付手续费的地址（可选）

        返回：
            交易结果字典

        注意：
            成功质押后，区块链将自动铸造一个质押凭证（NFT）给质押者。
        """
        # 质押通常为单一代币
        if len(amount) != 1:
            raise MedianSDKError("质押金额必须为单个代币类型")

        # 余额预检查 (质押金额)
        try:
            self._check_balance(delegator_address, int(amount[0].amount), amount[0].denom, "质押")
        except MedianSDKError:
            raise
        except Exception:
            pass

        msg = {
            "delegator_address": delegator_address,
            "validator_address": validator_address,
            "amount": [amount[0].to_dict()]
        }
        return self._broadcast_tx(
            "/cosmos.staking.v1beta1.MsgDelegate", msg, delegator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def undelegate_tokens(
        self,
        delegator_address: str,
        validator_address: str,
        amount: List[Coin],
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        从验证者解押代币

        参数：
            delegator_address: 质押者地址
            validator_address: 验证者地址
            amount: 代币金额列表（通常为单个代币）
            private_key: 质押者私钥
            wait_confirm: 是否等待交易确认
            fee_granter: 代付手续费的地址（可选）

        返回：
            交易结果字典
        """
        # 解押通常为单一代币
        if len(amount) != 1:
            raise MedianSDKError("解押金额必须为单个代币类型")

        msg = {
            "delegator_address": delegator_address,
            "validator_address": validator_address,
            "amount": [amount[0].to_dict()]
        }
        return self._broadcast_tx(
            "/cosmos.staking.v1beta1.MsgUndelegate", msg, delegator_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def get_delegation(
        self,
        delegator_address: str,
        validator_address: str
    ) -> Dict[str, Any]:
        """
        查询特定委托信息

        参数：
            delegator_address: 质押者地址
            validator_address: 验证者地址

        返回：
            委托信息字典
        """
        endpoint = f"/cosmos/staking/v1beta1/validators/{validator_address}/delegations/{delegator_address}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_delegator_delegations(
        self,
        delegator_address: str
    ) -> Dict[str, Any]:
        """
        查询质押者的所有委托

        参数：
            delegator_address: 质押者地址

        返回：
            委托列表字典
        """
        endpoint = f"/cosmos/staking/v1beta1/delegations/{delegator_address}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_unbonding_delegations(
        self,
        delegator_address: str,
        validator_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询解押中的委托

        参数：
            delegator_address: 质押者地址
            validator_address: 验证者地址（可选，如果提供则查询特定验证者）

        返回：
            解押中委托列表字典
        """
        suffix = f"/{validator_address}" if validator_address else ""
        endpoint = f"/cosmos/staking/v1beta1/delegators/{delegator_address}/unbonding_delegations{suffix}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_validator_delegations(
        self,
        validator_address: str
    ) -> Dict[str, Any]:
        """
        查询验证者的所有委托

        参数：
            validator_address: 验证者地址

        返回：
            委托列表字典
        """
        endpoint = f"/cosmos/staking/v1beta1/validators/{validator_address}/delegations"
        return self._make_request("GET", endpoint, raise_on_error=False)

    # ==================== NFT Methods ====================

    def is_nft_module_available(self) -> bool:
        """
        Check if the NFT module is available on the blockchain node.

        Returns:
            True if NFT module is available, False otherwise
        """
        try:
            result = self.get_nft_classes()
            return isinstance(result, dict) and "classes" in result and "error" not in result and "code" not in result
        except Exception:
            return False

    def get_nft(self, class_id: str, nft_id: str) -> Dict[str, Any]:
        """
        查询特定NFT

        参数：
            class_id: NFT类ID
            nft_id: NFT ID

        返回：
            NFT信息字典
        """
        endpoint = f"/cosmos/nft/v1beta1/nfts/{class_id}/{nft_id}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_nft_class(self, class_id: str) -> Dict[str, Any]:
        """
        查询NFT类信息

        参数：
            class_id: NFT类ID

        返回：
            NFT类信息字典
        """
        endpoint = f"/cosmos/nft/v1beta1/classes/{class_id}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_nft_classes(self) -> Dict[str, Any]:
        """
        查询所有NFT类

        返回：
            NFT类列表字典
        """
        endpoint = "/cosmos/nft/v1beta1/classes"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_nfts_by_owner(self, owner_address: str) -> Dict[str, Any]:
        """
        查询所有者的NFT

        参数：
            owner_address: 所有者地址

        返回：
            NFT列表字典
        """
        if not owner_address:
            raise MedianSDKError("owner_address cannot be empty")
        endpoint = f"/cosmos/nft/v1beta1/owners/{owner_address}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_nfts_by_class(self, class_id: str) -> Dict[str, Any]:
        """
        查询特定类的所有NFT

        参数：
            class_id: NFT类ID

        返回：
            NFT列表字典
        """
        endpoint = f"/cosmos/nft/v1beta1/nfts/{class_id}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_nft_supply(self, class_id: str) -> Dict[str, Any]:
        """
        查询NFT类的供应量

        参数：
            class_id: NFT类ID

        返回：
            供应量信息字典
        """
        endpoint = f"/cosmos/nft/v1beta1/supply/{class_id}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def mint_nft(
        self,
        sender_address: str,
        class_id: str,
        nft_id: str,
        uri: str,
        uri_hash: str,
        recipient: str,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        铸造一个新的NFT

        参数：
            sender_address: 发送方地址
            class_id: NFT类ID
            nft_id: NFT ID
            uri: 元数据URI
            uri_hash: 元数据哈希
            recipient: 接收方地址
            private_key: 发送方私钥
            wait_confirm: 是否等待交易确认
            fee_granter: 代付手续费的地址（可选）

        返回：
            交易结果字典
        """
        msg = {
            "sender": sender_address,
            "class_id": class_id,
            "id": nft_id,
            "uri": uri,
            "uri_hash": uri_hash,
            "recipient": recipient
        }
        return self._broadcast_tx(
            "/median.median.MsgMintNFT", msg, sender_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    # ==================== Certificate Methods ====================

    # Note: issue_staking_certificate is removed in v1.6.0.
    # Certificates are now automatically minted by the blockchain when delegating.

    def redeem_certificate(
        self,
        certificate_id: str,
        owner_address: str,
        class_id: str = "staking-certificate",
        burn_on_redeem: bool = True,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        赎回凭证并作废

        参数：
            certificate_id: 凭证ID
            owner_address: 凭证所有者地址
            class_id: NFT类ID（默认 "staking-certificate"）
            burn_on_redeem: 赎回时是否销毁NFT（默认True）
            private_key: 所有者私钥
            wait_confirm: 是否等待交易确认
            fee_granter: 代付手续费的地址（可选）

        返回：
            交易结果字典
        """
        # Check if NFT module is available
        if not self.is_nft_module_available():
            raise MedianSDKError("NFT module is not available on the blockchain node. Cannot redeem certificate.")

        msg_type = "/cosmos.nft.v1beta1.MsgBurnNFT" if burn_on_redeem else "/cosmos.nft.v1beta1.MsgSend"
        msg = {
            "sender": owner_address,
            "class_id": class_id,
            "id": certificate_id
        }

        if not burn_on_redeem:
            msg["recipient"] = "median1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"

        return self._broadcast_tx(
            msg_type, msg, owner_address, private_key,
            wait_confirm, gas, fee_amount, fee_denom, fee_granter, auto_estimate_gas
        )

    def query_certificates(
        self,
        owner_address: str,
        class_id: Optional[str] = "staking-certificate",
        active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        查询用户拥有的凭证

        参数：
            owner_address: 所有者地址
            class_id: NFT类ID（可选，默认 "staking-certificate"）
            active_only: 是否只返回活跃凭证（默认True）

        返回：
            凭证列表
        """
        # Check if NFT module is available
        if not self.is_nft_module_available():
            # If NFT module is not available, return empty list
            return []

        try:
            nfts_response = self.get_nfts_by_owner(owner_address)
            nfts = nfts_response.get("nfts", [])

            certificates = []
            for nft in nfts:
                nft_class_id = nft.get("class_id", "")
                nft_id = nft.get("id", "")

                # 如果指定了class_id，只返回匹配的NFT
                if class_id and nft_class_id != class_id:
                    continue

                # 解析元数据
                metadata = self._parse_nft_metadata(nft.get("uri", "{}"))

                # 如果要求只返回活跃凭证，检查状态
                if active_only and metadata.get("status", "active") != "active":
                    continue

                certificate = {
                    "certificate_id": nft_id,
                    "class_id": nft_class_id,
                    "owner": owner_address,
                    "metadata": metadata,
                    "nft_info": nft
                }
                certificates.append(certificate)

            return certificates
        except Exception:
            # 如果查询失败，返回空列表
            return []

    def get_certificate(
        self,
        certificate_id: str,
        class_id: str = "staking-certificate"
    ) -> Dict[str, Any]:
        """
        查询特定凭证详细信息

        参数：
            certificate_id: 凭证ID
            class_id: NFT类ID（默认 "staking-certificate"）

        返回：
            凭证详细信息字典
        """
        try:
            nft_info = self.get_nft(class_id, certificate_id)
            metadata = self._parse_nft_metadata(nft_info.get("uri", "{}"))

            return {
                "certificate_id": certificate_id,
                "class_id": class_id,
                "owner": nft_info.get("owner", ""),
                "metadata": metadata,
                "nft_info": nft_info
            }
        except Exception as e:
            raise MedianSDKError(f"查询凭证失败: {e}")

    # ==================== Fee Grant Methods ====================

    def grant_fee_allowance(
        self,
        granter_address: str,
        grantee_address: str,
        spend_limit: Optional[List[Coin]] = None,
        expiration: Optional[str] = None,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        Grant fee allowance to another account (feegrant).
        Uses BasicAllowance by default.

        Args:
            granter_address: The address granting the allowance
            grantee_address: The address receiving the allowance
            spend_limit: Optional list of coins to limit the spending
            expiration: Optional timestamp for expiration (RFC 3339 format)
            private_key: Granter's private key
            wait_confirm: Whether to wait for transaction confirmation
            fee_granter: 代付手续费的地址（可选）

        Returns:
            Transaction result
        """
        if feegrant_tx is None or feegrant_pb is None:
            raise MedianSDKError("Feegrant protobuf modules not found. Please install cosmospy-protobuf.")

        from google.protobuf.json_format import ParseDict

        # Create BasicAllowance
        allowance = feegrant_pb.BasicAllowance()
        allowance_dict = {}
        if spend_limit:
            allowance_dict["spend_limit"] = [coin.to_dict() for coin in spend_limit]
        
        if expiration:
            allowance_dict["expiration"] = expiration

        ParseDict(allowance_dict, allowance)

        # Pack into Any
        allowance_any = AnyPb()
        allowance_any.Pack(allowance)
        # Override type_url to match Cosmos SDK expectation (if needed, usually works with standard too)
        # But to be safe and consistent with previous behavior:
        allowance_any.type_url = "/cosmos.feegrant.v1beta1.BasicAllowance"

        # Create MsgGrantAllowance
        msg = feegrant_tx.MsgGrantAllowance()
        msg.granter = granter_address
        msg.grantee = grantee_address
        msg.allowance.CopyFrom(allowance_any)

        return self._broadcast_tx(
            msg_type="/cosmos.feegrant.v1beta1.MsgGrantAllowance",
            msg_content=msg,
            sender_address=granter_address,
            private_key=private_key,
            wait_confirm=wait_confirm,
            gas=gas,
            fee_amount=fee_amount,
            fee_denom=fee_denom,
            fee_granter=fee_granter,
            auto_estimate_gas=auto_estimate_gas
        )

    def revoke_fee_allowance(
        self,
        granter_address: str,
        grantee_address: str,
        private_key: Optional[str] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        Revoke fee allowance from an account.

        Args:
            granter_address: The address that granted the allowance
            grantee_address: The address to revoke the allowance from
            private_key: Granter's private key
            wait_confirm: Whether to wait for transaction confirmation
            fee_granter: 代付手续费的地址（可选）

        Returns:
            Transaction result
        """
        if feegrant_tx is None:
            raise MedianSDKError("Feegrant protobuf modules not found. Please install cosmospy-protobuf.")

        msg = feegrant_tx.MsgRevokeAllowance()
        msg.granter = granter_address
        msg.grantee = grantee_address

        return self._broadcast_tx(
            msg_type="/cosmos.feegrant.v1beta1.MsgRevokeAllowance",
            msg_content=msg,
            sender_address=granter_address,
            private_key=private_key,
            wait_confirm=wait_confirm,
            gas=gas,
            fee_amount=fee_amount,
            fee_denom=fee_denom,
            fee_granter=fee_granter,
            auto_estimate_gas=auto_estimate_gas
        )

    def get_fee_allowance(self, grantee_address: str, granter_address: str) -> Dict[str, Any]:
        """
        Query fee allowance for a specific granter-grantee pair.
        """
        endpoint = f"/cosmos/feegrant/v1beta1/allowance/{granter_address}/{grantee_address}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_allowances(self, grantee_address: str) -> Dict[str, Any]:
        """
        Query all fee allowances granted to an account.
        """
        endpoint = f"/cosmos/feegrant/v1beta1/allowances/{grantee_address}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    # ==================== Transaction Methods ====================

    def get_tx(self, tx_hash: str) -> Dict[str, Any]:
        """Query transaction by hash"""
        endpoint = f"/cosmos/tx/v1beta1/txs/{tx_hash}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def wait_for_tx(self, tx_hash: str, timeout: int = 30, interval: float = 1.0) -> Dict[str, Any]:
        """
        Wait for transaction to be included in a block.
        Returns transaction details when confirmed.

        Args:
            tx_hash: Transaction hash to wait for
            timeout: Maximum time to wait in seconds (default: 30)
            interval: Polling interval in seconds (default: 1.0)

        Returns:
            Transaction details

        Raises:
            MedianSDKError: If timeout is reached
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                tx = self.get_tx(tx_hash)
                tx_response = tx.get("tx_response", {})
                # If transaction is confirmed (has code field), return result
                if "code" in tx_response:
                    # Check for transaction errors
                    code = tx_response.get("code", 0)
                    if code != 0:
                        error_msg = f"Transaction failed (code={code}): {tx_response.get('raw_log', 'Unknown error')}"
                        raise MedianSDKError(error_msg)
                    return tx
            except MedianSDKError:
                raise
            except Exception:
                # Transaction might still be in mempool, continue waiting
                pass
            time.sleep(interval)
        raise MedianSDKError(f"Transaction confirmation timeout: {tx_hash}")

    # ==================== Distribution (Rewards) Methods ====================

    def get_delegator_rewards(
        self,
        delegator_address: str,
        validator_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询质押奖励

        参数：
            delegator_address: 质押者地址
            validator_address: 验证者地址（可选，如果提供则查询特定验证者的奖励）

        返回：
            奖励信息字典
        """
        suffix = f"/{validator_address}" if validator_address else ""
        endpoint = f"/cosmos/distribution/v1beta1/delegators/{delegator_address}/rewards{suffix}"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_validator_outstanding_rewards(
        self,
        validator_address: str
    ) -> Dict[str, Any]:
        """
        查询验证者的待分配奖励

        参数：
            validator_address: 验证者地址

        返回：
            待分配奖励信息字典
        """
        endpoint = f"/cosmos/distribution/v1beta1/validators/{validator_address}/outstanding_rewards"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_validator_commission(
        self,
        validator_address: str
    ) -> Dict[str, Any]:
        """
        查询验证者佣金

        参数：
            validator_address: 验证者地址

        返回：
            佣金信息字典
        """
        endpoint = f"/cosmos/distribution/v1beta1/validators/{validator_address}/commission"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_community_pool(self) -> Dict[str, Any]:
        """
        查询社区池余额

        返回：
            社区池余额信息字典
        """
        endpoint = "/cosmos/distribution/v1beta1/community_pool"
        return self._make_request("GET", endpoint, raise_on_error=False)

    def get_distribution_params(self) -> Dict[str, Any]:
        """
        查询分发模块参数

        返回：
            参数信息字典
        """
        endpoint = "/cosmos/distribution/v1beta1/params"
        return self._make_request("GET", endpoint, raise_on_error=False)

    # ==================== Batch Query Methods ====================

    def _batch_query(self, addresses: List[str], query_func, default_value):
        """Generic batch query helper."""
        result = {}
        for address in addresses:
            query_result = self._safe_query(query_func, address)
            result[address] = query_result if query_result is not None else default_value
        return result

    def _safe_query(self, func, *args):
        """Safely execute a query function, returning None on error."""
        try:
            return func(*args)
        except Exception:
            return None

    def batch_get_balances(self, addresses: List[str]) -> Dict[str, List[Coin]]:
        """批量查询多个地址的余额"""
        result = {}
        for address in addresses:
            result[address] = self._safe_query(self.get_account_balance, address) or []
        return result

    def batch_get_delegations(self, delegator_addresses: List[str]) -> Dict[str, Dict[str, Any]]:
        """批量查询多个质押者的委托信息"""
        result = {}
        for address in delegator_addresses:
            result[address] = self._safe_query(self.get_delegator_delegations, address) or {}
        return result

    def batch_get_certificates(
        self,
        owner_addresses: List[str],
        class_id: Optional[str] = "staking-certificate",
        active_only: bool = True
    ) -> Dict[str, List[Dict[str, Any]]]:
        """批量查询多个所有者的凭证"""
        result = {}
        for address in owner_addresses:
            result[address] = self._safe_query(self.query_certificates, address, class_id, active_only) or []
        return result

    # ==================== Composite Query Methods ====================

    def get_staking_summary(
        self,
        delegator_address: str
    ) -> Dict[str, Any]:
        """
        获取质押综合摘要信息

        包括：
        1. 质押总额
        2. 各个验证者的质押详情
        3. 解押中的质押
        4. 质押奖励
        5. 凭证信息

        参数：
            delegator_address: 质押者地址

        返回：
            综合摘要信息字典
        """
        summary = {
            "delegator_address": delegator_address,
            "total_staked": [],
            "delegations": {},
            "unbonding_delegations": {},
            "rewards": {},
            "certificates": [],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        try:
            # 查询委托信息
            delegations = self.get_delegator_delegations(delegator_address)
            delegation_list = delegations.get("delegation_responses", [])
            summary["delegations"] = delegation_list

            # 计算质押总额
            total_staked = {}
            for delegation in delegation_list:
                balance = delegation.get("balance", {})
                denom = balance.get("denom", "")
                amount = balance.get("amount", "0")
                if denom:
                    total_staked[denom] = total_staked.get(denom, 0) + int(amount)

            summary["total_staked"] = [
                Coin(denom=denom, amount=str(amount))
                for denom, amount in total_staked.items()
            ]

            # 查询解押中的质押
            unbonding = self.get_unbonding_delegations(delegator_address)
            summary["unbonding_delegations"] = unbonding.get("unbonding_responses", [])

            # 查询质押奖励
            rewards = self.get_delegator_rewards(delegator_address)
            summary["rewards"] = rewards

            # 查询凭证
            certificates = self.query_certificates(delegator_address)
            summary["certificates"] = certificates

        except Exception as e:
            summary["error"] = str(e)

        return summary

    def get_validator_summary(
        self,
        validator_address: str
    ) -> Dict[str, Any]:
        """
        获取验证者综合摘要信息

        包括：
        1. 验证者详情
        2. 总委托量
        3. 委托者列表
        4. 待分配奖励
        5. 佣金信息

        参数：
            validator_address: 验证者地址

        返回：
            验证者综合摘要信息字典
        """
        summary = {
            "validator_address": validator_address,
            "delegations": {},
            "total_delegated": [],
            "outstanding_rewards": {},
            "commission": {},
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        try:
            # 查询验证者委托
            delegations = self.get_validator_delegations(validator_address)
            summary["delegations"] = delegations

            # 计算总委托量
            delegation_responses = delegations.get("delegation_responses", [])
            total_delegated = {}
            for delegation in delegation_responses:
                balance = delegation.get("balance", {})
                denom = balance.get("denom", "")
                amount = balance.get("amount", "0")
                if denom:
                    total_delegated[denom] = total_delegated.get(denom, 0) + int(amount)

            summary["total_delegated"] = [
                Coin(denom=denom, amount=str(amount))
                for denom, amount in total_delegated.items()
            ]

            # 查询待分配奖励
            outstanding_rewards = self.get_validator_outstanding_rewards(validator_address)
            summary["outstanding_rewards"] = outstanding_rewards

            # 查询佣金
            commission = self.get_validator_commission(validator_address)
            summary["commission"] = commission

        except Exception as e:
            summary["error"] = str(e)

        return summary

    # ==================== Utility Methods ====================

    def _get_balance_for_denom(self, address: str, denom: str) -> int:
        """Get balance for a specific denomination."""
        try:
            balances = self.get_account_balance(address)
            for bal in balances:
                if bal.denom == denom:
                    return int(bal.amount)
            return 0
        except Exception:
            return 0

    def _check_balance(self, address: str, required_amount: int, denom: str, purpose: str = "操作") -> None:
        """Check if account has sufficient balance."""
        available = self._get_balance_for_denom(address, denom)
        if available < required_amount:
            raise MedianSDKError(
                f"余额不足以{purpose}: 需要 {required_amount} {denom}, "
                f"当前可用 {available} {denom}"
            )

    def _select_fee_denom(self, balances: List[Coin], default_denom: str, estimated_fee: int, user_specified: Optional[str]) -> str:
        """Select the best fee denomination based on available balances."""
        if user_specified:
            return user_specified

        # Check if default denom has sufficient balance
        default_balance = next((int(c.amount) for c in balances if c.denom == default_denom), 0)
        if default_balance >= estimated_fee:
            return default_denom

        # Find alternative denom with sufficient balance
        for coin in balances:
            if coin.denom != default_denom and int(coin.amount) >= estimated_fee:
                return coin.denom

        return default_denom

    def _parse_nft_metadata(self, uri: str) -> Dict[str, Any]:
        """Parse NFT metadata from URI string."""
        try:
            return json.loads(uri)
        except Exception:
            return {}

    def _check_tx_result(self, result: Dict[str, Any]) -> None:
        """
        Check transaction result, raise exception if failed.
        Provides helpful messages for sequence mismatch errors.
        """
        code = result.get("code", 0)
        if code != 0:
            codespace = result.get("codespace", "")
            raw_log = result.get("raw_log", "")
            error_msg = f"Transaction failed (code={code}, codespace={codespace}): {raw_log}"

            # Check for sequence error
            if "sequence" in raw_log.lower() or code == 32:
                error_msg += "\nHint: This may be an account sequence mismatch."
                error_msg += "\nPossible causes:"
                error_msg += "\n1. Previous transaction still in mempool"
                error_msg += "\n2. Account sequence number cache expired"
                error_msg += "\nSuggestion: Wait a few seconds and retry, or query latest account sequence"

            raise MedianSDKError(error_msg)

    def simulate_tx(
        self,
        msg_type: str,
        msg_content: Dict[str, Any],
        sender_address: str,
        private_key: Optional[Union[str, bytes]] = None
    ) -> int:
        """
        Simulate a transaction to estimate gas usage.

        Args:
            msg_type: The protobuf message type
            msg_content: The message content
            sender_address: The sender's address
            private_key: The sender's private key

        Returns:
            Estimated gas units required

        Raises:
            MedianSDKError: If simulation fails
        """
        if not private_key:
            raise ValueError("Private key is required for simulating transactions")

        # Handle private key conversion
        try:
            if isinstance(private_key, bytes):
                pk_bytes = private_key
            elif isinstance(private_key, str):
                clean_key = private_key.replace("0x", "")
                pk_bytes = bytes.fromhex(clean_key)
            else:
                raise ValueError(f"Unsupported private key type: {type(private_key)}")
        except Exception as e:
            raise ValueError(f"Invalid private key format: {e}")

        # Create account instance
        hrp = sender_address.split('1')[0]
        account = Account(
            private_key=pk_bytes.hex(),
            hrp=hrp,
            protobuf="cosmos"
        )

        # Sync account info
        acc_info = self.get_account(sender_address)
        base_acc = acc_info.get("account", {})
        if "base_vesting_account" in base_acc:
            base_acc = base_acc["base_vesting_account"]["base_account"]

        account.account_number = int(base_acc.get("account_number", 0))
        account.next_sequence = int(base_acc.get("sequence", 0))

        # Create transaction with minimal gas for simulation
        tx = Transaction(
            account=account,
            chain_id=self.chain_id,
            gas=0  # Will be estimated by simulation
        )

        # Set minimal fee for simulation
        tx.set_fee(amount=1, denom=self.default_fee_denom)

        # Add message
        tx.add_dict_msg(msg_content, msg_type)

        # Get transaction bytes for simulation
        if hasattr(tx, 'get_tx_bytes_base64'):
            tx_bytes_base64 = tx.get_tx_bytes_base64()
        else:
            tx_bytes = tx.get_tx_bytes()
            tx_bytes_base64 = base64.b64encode(tx_bytes).decode('utf-8')

        # Call simulate endpoint
        payload = {
            "tx_bytes": tx_bytes_base64
        }

        endpoint = "/cosmos/tx/v1beta1/simulate"
        try:
            result = self._make_request("POST", endpoint, data=payload)
            gas_info = result.get("gas_info", {})
            gas_used = int(gas_info.get("gas_used", 0))

            if gas_used == 0:
                raise MedianSDKError("Simulation returned zero gas estimate")

            return gas_used
        except Exception as e:
            raise MedianSDKError(f"Transaction simulation failed: {e}")

    def _broadcast_tx(
        self,
        msg_type: str,
        msg_content: Union[Dict[str, Any], ProtoMessage],
        sender_address: str,
        private_key: Optional[Union[str, bytes]] = None,
        wait_confirm: bool = False,
        gas: Optional[int] = None,
        fee_amount: Optional[int] = None,
        fee_denom: Optional[str] = None,
        fee_granter: Optional[str] = None,
        auto_estimate_gas: bool = False
    ) -> Dict[str, Any]:
        """
        Broadcast a signed transaction using mospy.
        Optionally wait for transaction confirmation.

        Args:
            msg_type: The protobuf message type
            msg_content: The message content (dict or Protobuf Message)
            sender_address: The sender's address
            private_key: The sender's private key
            wait_confirm: Whether to wait for transaction confirmation
            gas: Gas limit (optional, will use default if not provided)
            fee_amount: Fee amount (optional, will use default if not provided)
            fee_denom: Fee denomination (optional, will use default if not provided)
            fee_granter: Address of the fee granter (optional)
            auto_estimate_gas: If True, automatically estimate gas via simulation

        Returns:
            Transaction result
        """
        if not private_key:
            raise ValueError("Private key is required for signing transactions")

        # Handle private key conversion
        try:
            if isinstance(private_key, bytes):
                pk_bytes = private_key
            elif isinstance(private_key, str):
                # Remove 0x prefix if present
                clean_key = private_key.replace("0x", "")
                pk_bytes = bytes.fromhex(clean_key)
            else:
                raise ValueError(f"Unsupported private key type: {type(private_key)}")
        except Exception as e:
             raise ValueError(f"Invalid private key format: {e}")

        # Create account instance
        hrp = sender_address.split('1')[0]

        account = Account(
            private_key=pk_bytes.hex(),
            hrp=hrp,
            protobuf="cosmos"
        )

        # Sync account info (sequence, account number) from chain
        acc_info = self.get_account(sender_address)
        base_acc = acc_info.get("account", {})
        # Handle nesting
        if "base_vesting_account" in base_acc:
            base_acc = base_acc["base_vesting_account"]["base_account"]

        account_number = int(base_acc.get("account_number", 0))
        sequence = int(base_acc.get("sequence", 0))

        if account_number == 0 and sequence == 0 and not base_acc:
             raise MedianSDKError(f"账户 {sender_address} 在链上不存在，请先发送一些代币到该地址。")

        account.account_number = account_number
        account.next_sequence = sequence

        # Fetch balances once for fee decision and pre-check
        account_balances = []
        try:
            account_balances = self.get_account_balance(sender_address)
        except Exception:
            pass

        # Estimate fee amount for denom selection (heuristic)
        # Use provided fee or estimate based on gas price
        estimated_fee_amount = fee_amount
        if estimated_fee_amount is None:
            # Fallback to gas * price estimation
            est_gas = gas if gas is not None else self.default_gas
            estimated_fee_amount = math.ceil(est_gas * self.gas_price)

        # Determine actual fee denom (Smart Selection)
        actual_fee_denom = self._select_fee_denom(
            account_balances, self.default_fee_denom, estimated_fee_amount, fee_denom
        )

        # Determine actual gas and fee
        if auto_estimate_gas:
            try:
                # Simulate transaction to get gas estimate
                # NOTE: For simulation, if using a raw ProtoMessage, we might need special handling
                # For now, simplistic simulation logic is kept
                estimated_gas = self.simulate_tx(
                    msg_type=msg_type,
                    msg_content=msg_content if isinstance(msg_content, dict) else {}, # Simulate might fail with raw msg
                    sender_address=sender_address,
                    private_key=private_key
                )
                actual_gas = math.ceil(estimated_gas * self.gas_adjustment)
                if gas is not None and actual_gas > gas:
                    actual_gas = gas
                
                # Dynamic fee calculation
                if fee_amount is None:
                    actual_fee_amount = math.ceil(actual_gas * self.gas_price)
                else:
                    actual_fee_amount = fee_amount
            except Exception as e:
                # Fallback
                actual_gas = gas if gas is not None else self.default_gas
                actual_fee_amount = fee_amount if fee_amount is not None else math.ceil(actual_gas * self.gas_price)
        else:
            actual_gas = gas if gas is not None else self.default_gas
            # Even without auto-estimation, fee should be proportional to gas if not specified
            if fee_amount is not None:
                actual_fee_amount = fee_amount
            else:
                actual_fee_amount = math.ceil(actual_gas * self.gas_price)

        # Final Balance Pre-check (for fee)
        # Skip check if fee granter is used
        if not fee_granter:
            fee_coin_balance = 0
            for coin in account_balances:
                if coin.denom == actual_fee_denom:
                    fee_coin_balance = int(coin.amount)
                    break
            
            if fee_coin_balance < actual_fee_amount:
                all_balances_str = ", ".join([f"{c.amount} {c.denom}" for c in account_balances])
                error_msg = (
                    f"余额不足以支付手续费: 需要 {actual_fee_amount} {actual_fee_denom}, "
                    f"当前余额 {fee_coin_balance} {actual_fee_denom}。"
                )
                if all_balances_str:
                    error_msg += f" (账户当前全部余额: {all_balances_str})"
                
                raise MedianSDKError(error_msg)

        tx = Transaction(
            account=account,
            chain_id=self.chain_id,
            gas=actual_gas,
            feegrant=fee_granter or ""
        )

        # Set fee (required for mospy 0.6.0)
        tx.set_fee(amount=actual_fee_amount, denom=actual_fee_denom)

        # Add Message
        if isinstance(msg_content, ProtoMessage):
            tx.add_raw_msg(msg_content, type_url=msg_type)
        else:
            tx.add_dict_msg(msg_content, msg_type)

        # Get transaction bytes
        # Try get_tx_bytes_base64 first, fallback to get_tx_bytes + base64 encode
        if hasattr(tx, 'get_tx_bytes_base64'):
            tx_bytes_base64 = tx.get_tx_bytes_base64()
        else:
            tx_bytes = tx.get_tx_bytes()
            tx_bytes_base64 = base64.b64encode(tx_bytes).decode('utf-8')

        payload = {
            "tx_bytes": tx_bytes_base64,
            "mode": "BROADCAST_MODE_SYNC"
        }

        endpoint = "/cosmos/tx/v1beta1/txs"
        result = self._make_request("POST", endpoint, data=payload)

        # Extract tx_hash from response
        tx_response = result.get("tx_response", {})
        tx_hash = tx_response.get("txhash", "")

        # Check for immediate failures
        self._check_tx_result(tx_response)

        # If wait_confirm is True, wait for transaction to be included
        if wait_confirm and tx_hash:
            try:
                confirmed_tx = self.wait_for_tx(tx_hash, timeout=30)
                confirmed_response = confirmed_tx.get("tx_response", {})
                self._check_tx_result(confirmed_response)
                return {"txhash": tx_hash, "confirmed": True, **confirmed_response}
            except MedianSDKError:
                # Return original result if wait fails
                return result

        # Add txhash to result for consistency
        if tx_hash:
            result["txhash"] = tx_hash
        return result


def create_sdk(
    api_url: str = "http://localhost:1317",
    chain_id: str = "median"
) -> MedianSDK:
    return MedianSDK(api_url=api_url, chain_id=chain_id)
