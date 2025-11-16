from datetime import datetime
from typing import List, Optional
import json


class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0.0, 
                 account_holder: str = "Unknown", max_overdraft: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        if max_overdraft < 0:
            raise ValueError("Max overdraft cannot be negative")
            
        self._account_number = account_number
        self._balance = initial_balance
        self._account_holder = account_holder
        self._max_overdraft = max_overdraft
        self._transaction_history: List[dict] = []
        self._is_active = True
        self._last_transaction_date: Optional[datetime] = None
        
        self._add_transaction("INITIAL", initial_balance, "Account opened")
    
    @property
    def account_number(self) -> str:
        return self._account_number
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def account_holder(self) -> str:
        return self._account_holder
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def transaction_history(self) -> List[dict]:
        return self._transaction_history.copy()
    
    @property
    def available_balance(self) -> float:
        return self._balance + self._max_overdraft
    
    def deposit(self, amount: float, description: str = "Deposit") -> bool:
        if not self._is_active:
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self._add_transaction("DEPOSIT", amount, description)
        return True
    
    def withdraw(self, amount: float, description: str = "Withdrawal") -> bool:
        if not self._is_active:
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self._balance - amount < -self._max_overdraft:
            raise ValueError("Insufficient funds")
        
        self._balance -= amount
        self._add_transaction("WITHDRAWAL", -amount, description)
        return True
    
    def transfer_to(self, target_account: 'BankAccount', amount: float, 
                   description: str = "Transfer") -> bool:
        if not self._is_active:
            raise ValueError("Source account is not active")
        if not target_account._is_active:
            raise ValueError("Target account is not active")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        
        self.withdraw(amount, f"Transfer to {target_account.account_number}")
        
        target_account.deposit(amount, f"Transfer from {self._account_number}")
        
        return True
    
    def get_balance_statement(self) -> dict:
        return {
            "account_number": self._account_number,
            "account_holder": self._account_holder,
            "current_balance": self._balance,
            "available_balance": self.available_balance,
            "max_overdraft": self._max_overdraft,
            "is_active": self._is_active,
            "last_transaction": self._last_transaction_date.isoformat() if self._last_transaction_date else None,
            "total_transactions": len(self._transaction_history)
        }
    
    def freeze_account(self) -> bool:
        if not self._is_active:
            return False
        
        self._is_active = False
        self._add_transaction("FREEZE", 0, "Account frozen")
        return True
    
    def unfreeze_account(self) -> bool:
        if self._is_active:
            return False
        
        self._is_active = True
        self._add_transaction("UNFREEZE", 0, "Account unfrozen")
        return True
    
    def set_max_overdraft(self, new_limit: float) -> bool:
        if new_limit < 0:
            raise ValueError("Overdraft limit cannot be negative")
        
        old_limit = self._max_overdraft
        self._max_overdraft = new_limit
        self._add_transaction("OVERDRAFT_CHANGE", 0, 
                             f"Overdraft limit changed from {old_limit} to {new_limit}")
        return True
    
    def _add_transaction(self, transaction_type: str, amount: float, description: str):
        transaction = {
            "timestamp": datetime.now(),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "balance_after": self._balance
        }
        self._transaction_history.append(transaction)
        self._last_transaction_date = transaction["timestamp"]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[dict]:
        return [t for t in self._transaction_history if t["type"] == transaction_type]
    
    def get_transactions_in_range(self, start_date: datetime, end_date: datetime) -> List[dict]:
        return [
            t for t in self._transaction_history
            if start_date <= t["timestamp"] <= end_date
        ]
