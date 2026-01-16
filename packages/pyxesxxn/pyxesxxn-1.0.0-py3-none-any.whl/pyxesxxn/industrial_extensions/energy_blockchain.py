"""
能源区块链与分布式交易模块

支持能源peer-to-peer交易的区块链集成，实现工业园区内的分布式能源交易
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib

from .base import (
    BaseIndustrialExtension,
    OptimizationObjective,
    OptimizationResult,
    EnergyCalculator,
    TimeSeriesGenerator,
    ResultAnalyzer
)


class TransactionStatus(Enum):
    """交易状态"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EnergyType(Enum):
    """能源类型"""
    ELECTRICITY = "electricity"
    HEAT = "heat"
    HYDROGEN = "hydrogen"
    NATURAL_GAS = "natural_gas"


@dataclass
class BlockchainNode:
    """区块链节点"""
    node_id: str
    node_type: str  # producer, consumer, prosumer
    location: str
    energy_capacity: float  # kW
    storage_capacity: Optional[float] = None  # kWh
    reputation_score: float = 1.0
    public_key: str = ""
    private_key: str = ""


@dataclass
class EnergyTransaction:
    """能源交易"""
    transaction_id: str
    seller_id: str
    buyer_id: str
    energy_type: EnergyType
    energy_amount: float  # kWh
    price: float  # 元/kWh
    timestamp: datetime
    status: TransactionStatus = TransactionStatus.PENDING
    blockchain_hash: str = ""
    smart_contract: Optional[Dict[str, Any]] = None
    verification_count: int = 0


@dataclass
class SmartContract:
    """智能合约"""
    contract_id: str
    contract_type: str  # spot_market, forward_contract, ppa
    parties: List[str]
    terms: Dict[str, Any]
    execution_conditions: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime] = None
    status: str = "active"


@dataclass
class EnergyOffer:
    """能源报价"""
    offer_id: str
    seller_id: str
    energy_type: EnergyType
    energy_amount: float  # kWh
    price: float  # 元/kWh
    available_from: datetime
    available_until: datetime
    location: str
    quality_score: float = 1.0


@dataclass
class EnergyBid:
    """能源出价"""
    bid_id: str
    buyer_id: str
    energy_type: EnergyType
    energy_amount: float  # kWh
    max_price: float  # 元/kWh
    required_from: datetime
    required_until: datetime
    location: str
    priority: int = 1


class Blockchain:
    """区块链实现"""
    
    def __init__(self, chain_id: str, difficulty: int = 4):
        self.chain_id = chain_id
        self.difficulty = difficulty
        self.chain: List[Dict[str, Any]] = []
        self.pending_transactions: List[EnergyTransaction] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """创建创世区块"""
        genesis_block = {
            'index': 0,
            'timestamp': datetime.now(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0,
            'hash': self.calculate_hash(0, datetime.now(), [], '0', 0)
        }
        self.chain.append(genesis_block)
    
    def calculate_hash(
        self,
        index: int,
        timestamp: datetime,
        transactions: List[EnergyTransaction],
        previous_hash: str,
        nonce: int
    ) -> str:
        """计算区块哈希值"""
        block_string = f"{index}{timestamp}{len(transactions)}{previous_hash}{nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, transactions: List[EnergyTransaction]) -> Dict[str, Any]:
        """挖矿创建新区块"""
        previous_block = self.chain[-1]
        new_index = previous_block['index'] + 1
        new_timestamp = datetime.now()
        previous_hash = previous_block['hash']
        
        nonce = 0
        while True:
            block_hash = self.calculate_hash(
                new_index, new_timestamp, transactions, previous_hash, nonce
            )
            if block_hash[:self.difficulty] == '0' * self.difficulty:
                break
            nonce += 1
        
        new_block = {
            'index': new_index,
            'timestamp': new_timestamp,
            'transactions': transactions,
            'previous_hash': previous_hash,
            'nonce': nonce,
            'hash': block_hash
        }
        
        self.chain.append(new_block)
        return new_block
    
    def add_transaction(self, transaction: EnergyTransaction):
        """添加交易到待处理列表"""
        self.pending_transactions.append(transaction)
    
    def is_chain_valid(self) -> bool:
        """验证区块链有效性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            
            recalculated_hash = self.calculate_hash(
                current_block['index'],
                current_block['timestamp'],
                current_block['transactions'],
                current_block['previous_hash'],
                current_block['nonce']
            )
            
            if recalculated_hash != current_block['hash']:
                return False
        
        return True


class EnergyBlockchainManager(BaseIndustrialExtension):
    """能源区块链管理器
    
    支持能源peer-to-peer交易的区块链集成，实现工业园区内的分布式能源交易
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化能源区块链管理器
        
        Parameters
        ----------
        config : Dict[str, Any], optional
            配置参数，包括：
            - blockchain: 区块链配置
            - nodes: 区块链节点列表
            - smart_contracts: 智能合约列表
            - offers: 能源报价列表
            - bids: 能源出价列表
        """
        super().__init__(config)
        
        self.blockchain: Optional[Blockchain] = None
        self.nodes: Dict[str, BlockchainNode] = {}
        self.smart_contracts: Dict[str, SmartContract] = {}
        self.offers: Dict[str, EnergyOffer] = {}
        self.bids: Dict[str, EnergyBid] = {}
        self.transactions: Dict[str, EnergyTransaction] = {}
        self.market_prices: Dict[str, float] = {}
        
        if config:
            self._load_config(config)
    
    def _load_config(self, config: Dict[str, Any]):
        """加载配置"""
        if 'blockchain' in config:
            blockchain_config = config['blockchain']
            self.blockchain = Blockchain(
                blockchain_config.get('chain_id', 'energy_chain'),
                blockchain_config.get('difficulty', 4)
            )
        
        if 'nodes' in config:
            for node_config in config['nodes']:
                node = BlockchainNode(**node_config)
                self.nodes[node.node_id] = node
        
        if 'smart_contracts' in config:
            for contract_config in config['smart_contracts']:
                contract = SmartContract(**contract_config)
                self.smart_contracts[contract.contract_id] = contract
        
        if 'offers' in config:
            for offer_config in config['offers']:
                offer = EnergyOffer(**offer_config)
                self.offers[offer.offer_id] = offer
        
        if 'bids' in config:
            for bid_config in config['bids']:
                bid = EnergyBid(**bid_config)
                self.bids[bid.bid_id] = bid
    
    def initialize(self) -> bool:
        """初始化模块
        
        Returns
        -------
        bool
            初始化是否成功
        """
        try:
            if self.blockchain is None:
                self.blockchain = Blockchain('energy_chain', 4)
            
            if not self.nodes:
                print("警告: 未配置区块链节点")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            return False
    
    def add_node(self, node: BlockchainNode):
        """添加区块链节点
        
        Parameters
        ----------
        node : BlockchainNode
            区块链节点
        """
        self.nodes[node.node_id] = node
    
    def create_smart_contract(
        self,
        contract_id: str,
        contract_type: str,
        parties: List[str],
        terms: Dict[str, Any],
        execution_conditions: Dict[str, Any],
        duration_days: int = 30
    ) -> SmartContract:
        """创建智能合约
        
        Parameters
        ----------
        contract_id : str
            合约ID
        contract_type : str
            合约类型
        parties : List[str]
            参与方
        terms : Dict[str, Any]
            合约条款
        execution_conditions : Dict[str, Any]
            执行条件
        duration_days : int
            有效期（天）
        
        Returns
        -------
        SmartContract
            智能合约
        """
        contract = SmartContract(
            contract_id=contract_id,
            contract_type=contract_type,
            parties=parties,
            terms=terms,
            execution_conditions=execution_conditions,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=duration_days),
            status="active"
        )
        
        self.smart_contracts[contract_id] = contract
        return contract
    
    def create_offer(
        self,
        seller_id: str,
        energy_type: EnergyType,
        energy_amount: float,
        price: float,
        available_from: datetime,
        available_until: datetime,
        location: str
    ) -> EnergyOffer:
        """创建能源报价
        
        Parameters
        ----------
        seller_id : str
            卖方ID
        energy_type : EnergyType
            能源类型
        energy_amount : float
            能源数量
        price : float
            价格
        available_from : datetime
            可用开始时间
        available_until : datetime
            可用结束时间
        location : str
            位置
        
        Returns
        -------
        EnergyOffer
            能源报价
        """
        offer_id = f"offer_{seller_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        offer = EnergyOffer(
            offer_id=offer_id,
            seller_id=seller_id,
            energy_type=energy_type,
            energy_amount=energy_amount,
            price=price,
            available_from=available_from,
            available_until=available_until,
            location=location,
            quality_score=self.nodes[seller_id].reputation_score if seller_id in self.nodes else 1.0
        )
        
        self.offers[offer_id] = offer
        return offer
    
    def create_bid(
        self,
        buyer_id: str,
        energy_type: EnergyType,
        energy_amount: float,
        max_price: float,
        required_from: datetime,
        required_until: datetime,
        location: str,
        priority: int = 1
    ) -> EnergyBid:
        """创建能源出价
        
        Parameters
        ----------
        buyer_id : str
            买方ID
        energy_type : EnergyType
            能源类型
        energy_amount : float
            能源数量
        max_price : float
            最高价格
        required_from : datetime
            需求开始时间
        required_until : datetime
            需求结束时间
        location : str
            位置
        priority : int
            优先级
        
        Returns
        -------
        EnergyBid
            能源出价
        """
        bid_id = f"bid_{buyer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        bid = EnergyBid(
            bid_id=bid_id,
            buyer_id=buyer_id,
            energy_type=energy_type,
            energy_amount=energy_amount,
            max_price=max_price,
            required_from=required_from,
            required_until=required_until,
            location=location,
            priority=priority
        )
        
        self.bids[bid_id] = bid
        return bid
    
    def match_trades(self) -> List[EnergyTransaction]:
        """匹配交易
        
        Returns
        -------
        List[EnergyTransaction]
            匹配的交易列表
        """
        matched_transactions = []
        
        for bid_id, bid in self.bids.items():
            best_offer = None
            best_score = -1
            
            for offer_id, offer in self.offers.items():
                if offer.energy_type != bid.energy_type:
                    continue
                
                if offer.energy_amount < bid.energy_amount:
                    continue
                
                if offer.price > bid.max_price:
                    continue
                
                if offer.available_from > bid.required_from:
                    continue
                
                if offer.available_until < bid.required_until:
                    continue
                
                score = self._calculate_match_score(offer, bid)
                if score > best_score:
                    best_score = score
                    best_offer = offer
            
            if best_offer:
                transaction = self._create_transaction(
                    best_offer.seller_id,
                    bid.buyer_id,
                    best_offer.energy_type,
                    bid.energy_amount,
                    best_offer.price
                )
                
                matched_transactions.append(transaction)
                
                del self.offers[best_offer.offer_id]
                del self.bids[bid_id]
        
        return matched_transactions
    
    def _calculate_match_score(self, offer: EnergyOffer, bid: EnergyBid) -> float:
        """计算匹配分数
        
        Parameters
        ----------
        offer : EnergyOffer
            报价
        bid : EnergyBid
            出价
        
        Returns
        -------
        float
            匹配分数
        """
        price_score = 1.0 - (offer.price / bid.max_price)
        quality_score = offer.quality_score
        time_score = 1.0
        
        time_diff = (offer.available_from - bid.required_from).total_seconds() / 3600
        if time_diff > 0:
            time_score = 1.0 / (1.0 + time_diff)
        
        total_score = 0.4 * price_score + 0.3 * quality_score + 0.3 * time_score
        return total_score
    
    def _create_transaction(
        self,
        seller_id: str,
        buyer_id: str,
        energy_type: EnergyType,
        energy_amount: float,
        price: float
    ) -> EnergyTransaction:
        """创建交易
        
        Parameters
        ----------
        seller_id : str
            卖方ID
        buyer_id : str
            买方ID
        energy_type : EnergyType
            能源类型
        energy_amount : float
            能源数量
        price : float
            价格
        
        Returns
        -------
        EnergyTransaction
            能源交易
        """
        transaction_id = f"tx_{seller_id}_{buyer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        transaction = EnergyTransaction(
            transaction_id=transaction_id,
            seller_id=seller_id,
            buyer_id=buyer_id,
            energy_type=energy_type,
            energy_amount=energy_amount,
            price=price,
            timestamp=datetime.now(),
            status=TransactionStatus.PENDING
        )
        
        self.transactions[transaction_id] = transaction
        return transaction
    
    def execute_transaction(self, transaction_id: str) -> bool:
        """执行交易
        
        Parameters
        ----------
        transaction_id : str
            交易ID
        
        Returns
        -------
        bool
            是否成功
        """
        if transaction_id not in self.transactions:
            return False
        
        transaction = self.transactions[transaction_id]
        
        if transaction.status != TransactionStatus.PENDING:
            return False
        
        if self.blockchain:
            self.blockchain.add_transaction(transaction)
            mined_block = self.blockchain.mine_block([transaction])
            transaction.blockchain_hash = mined_block['hash']
            transaction.verification_count = len(self.blockchain.chain)
        
        transaction.status = TransactionStatus.COMPLETED
        
        return True
    
    def optimize(
        self,
        objective: OptimizationObjective = OptimizationObjective.COST,
        time_horizon: int = 24,
        **kwargs
    ) -> OptimizationResult:
        """优化区块链交易
        
        Parameters
        ----------
        objective : OptimizationObjective
            优化目标
        time_horizon : int
            优化时间范围（小时）
        **kwargs
            其他参数
        
        Returns
        -------
        OptimizationResult
            优化结果
        """
        if not self.initialized:
            return OptimizationResult(
                success=False,
                objective_value=0.0,
                total_cost=0.0,
                total_carbon_emissions=0.0,
                energy_schedule={},
                component_utilization={},
                convergence_time=0.0,
                error_message="模块未初始化"
            )
        
        start_time = datetime.now()
        
        try:
            matched_transactions = self.match_trades()
            
            total_cost = 0.0
            total_carbon = 0.0
            energy_schedule = {}
            component_utilization = {}
            
            for transaction in matched_transactions:
                transaction_cost = transaction.energy_amount * transaction.price
                total_cost += transaction_cost
                
                if transaction.seller_id not in energy_schedule:
                    energy_schedule[transaction.seller_id] = []
                
                energy_schedule[transaction.seller_id].append({
                    'transaction_id': transaction.transaction_id,
                    'buyer_id': transaction.buyer_id,
                    'energy_type': transaction.energy_type.value,
                    'energy_amount': transaction.energy_amount,
                    'price': transaction.price,
                    'cost': transaction_cost,
                    'timestamp': transaction.timestamp
                })
            
            for node_id, node in self.nodes.items():
                utilization = 0.5 + np.random.random() * 0.4
                component_utilization[node_id] = utilization
            
            for contract_id, contract in self.smart_contracts.items():
                component_utilization[contract_id] = 0.7
            
            convergence_time = (datetime.now() - start_time).total_seconds()
            
            result = OptimizationResult(
                success=True,
                objective_value=total_cost,
                total_cost=total_cost,
                total_carbon_emissions=total_carbon,
                energy_schedule=energy_schedule,
                component_utilization=component_utilization,
                convergence_time=convergence_time,
                additional_metrics={
                    'cost_components': {
                        'transaction_fees': total_cost * 0.01,
                        'energy_cost': total_cost * 0.99
                    },
                    'emission_sources': {},
                    'matched_transactions': len(matched_transactions)
                }
            )
            
            self.results = {
                'optimization_result': result,
                'objective': objective,
                'time_horizon': time_horizon
            }
            
            return result
            
        except Exception as e:
            return OptimizationResult(
                success=False,
                objective_value=0.0,
                total_cost=0.0,
                total_carbon_emissions=0.0,
                energy_schedule={},
                component_utilization={},
                convergence_time=0.0,
                error_message=str(e)
            )
    
    def calculate_market_price(
        self,
        energy_type: EnergyType,
        location: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> float:
        """计算市场价格
        
        Parameters
        ----------
        energy_type : EnergyType
            能源类型
        location : str
            位置
        time_window : timedelta
            时间窗口
        
        Returns
        -------
        float
            市场价格
        """
        relevant_offers = [
            offer for offer in self.offers.values()
            if offer.energy_type == energy_type and
               offer.location == location and
               datetime.now() - offer.available_from <= time_window
        ]
        
        if not relevant_offers:
            return 0.8
        
        prices = [offer.price for offer in relevant_offers]
        return np.mean(prices)
    
    def get_node_reputation(self, node_id: str) -> float:
        """获取节点声誉
        
        Parameters
        ----------
        node_id : str
            节点ID
        
        Returns
        -------
        float
            声誉分数
        """
        if node_id not in self.nodes:
            return 0.0
        
        completed_transactions = [
            tx for tx in self.transactions.values()
            if (tx.seller_id == node_id or tx.buyer_id == node_id) and
               tx.status == TransactionStatus.COMPLETED
        ]
        
        if not completed_transactions:
            return self.nodes[node_id].reputation_score
        
        success_rate = len(completed_transactions) / max(len(self.transactions), 1)
        new_reputation = 0.7 * self.nodes[node_id].reputation_score + 0.3 * success_rate
        
        return new_reputation
    
    def generate_blockchain_report(self) -> Dict[str, Any]:
        """生成区块链报告
        
        Returns
        -------
        Dict[str, Any]
            区块链报告
        """
        if not self.results:
            return {'error': '未运行优化'}
        
        optimization_result = self.results['optimization_result']
        
        cost_analysis = ResultAnalyzer.analyze_cost_breakdown(optimization_result)
        utilization_analysis = ResultAnalyzer.analyze_utilization(optimization_result)
        
        report = {
            'summary': {
                'total_nodes': len(self.nodes),
                'total_smart_contracts': len(self.smart_contracts),
                'total_offers': len(self.offers),
                'total_bids': len(self.bids),
                'total_transactions': len(self.transactions),
                'blockchain_valid': self.blockchain.is_chain_valid() if self.blockchain else False,
                'optimization_objective': self.results['objective'],
                'time_horizon': self.results['time_horizon']
            },
            'cost_analysis': cost_analysis,
            'utilization_analysis': utilization_analysis,
            'node_details': {},
            'contract_details': {},
            'transaction_summary': {}
        }
        
        for node_id, node in self.nodes.items():
            report['node_details'][node_id] = {
                'type': node.node_type,
                'location': node.location,
                'energy_capacity': node.energy_capacity,
                'storage_capacity': node.storage_capacity,
                'reputation_score': self.get_node_reputation(node_id)
            }
        
        for contract_id, contract in self.smart_contracts.items():
            report['contract_details'][contract_id] = {
                'type': contract.contract_type,
                'parties': contract.parties,
                'status': contract.status,
                'created_at': contract.created_at,
                'expires_at': contract.expires_at
            }
        
        completed_transactions = [
            tx for tx in self.transactions.values()
            if tx.status == TransactionStatus.COMPLETED
        ]
        
        if completed_transactions:
            total_volume = sum(tx.energy_amount for tx in completed_transactions)
            total_value = sum(tx.energy_amount * tx.price for tx in completed_transactions)
            avg_price = total_value / total_volume if total_volume > 0 else 0
            
            report['transaction_summary'] = {
                'total_completed': len(completed_transactions),
                'total_volume': total_volume,
                'total_value': total_value,
                'average_price': avg_price
            }
        
        return report
    
    def export_blockchain_data(self, file_path: str) -> bool:
        """导出区块链数据
        
        Parameters
        ----------
        file_path : str
            文件路径
        
        Returns
        -------
        bool
            是否成功
        """
        if not self.blockchain:
            return False
        
        try:
            blockchain_data = {
                'chain_id': self.blockchain.chain_id,
                'difficulty': self.blockchain.difficulty,
                'chain_length': len(self.blockchain.chain),
                'is_valid': self.blockchain.is_chain_valid(),
                'blocks': [
                    {
                        'index': block['index'],
                        'timestamp': block['timestamp'],
                        'hash': block['hash'],
                        'previous_hash': block['previous_hash'],
                        'nonce': block['nonce'],
                        'transaction_count': len(block['transactions'])
                    }
                    for block in self.blockchain.chain
                ]
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(blockchain_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"导出失败: {str(e)}")
            return False