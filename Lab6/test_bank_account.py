import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    """Тесты для класса BankAccount"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.account = BankAccount("123456789", 1000.0, "John Doe", 500.0)
        self.empty_account = BankAccount("987654321", 0.0, "Jane Smith", 0.0)
    
    def test_initialization_success(self):
        """Тест успешной инициализации счета"""
        self.assertEqual(self.account.account_number, "123456789")
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.account_holder, "John Doe")
        self.assertTrue(self.account.is_active)
        self.assertEqual(len(self.account.transaction_history), 1)
        self.assertEqual(self.account.transaction_history[0]["type"], "INITIAL")
    
    def test_initialization_with_negative_balance(self):
        """Тест инициализации с отрицательным балансом"""
        with self.assertRaises(ValueError):
            BankAccount("123", -100.0)
    
    def test_initialization_with_negative_overdraft(self):
        """Тест инициализации с отрицательным овердрафтом"""
        with self.assertRaises(ValueError):
            BankAccount("123", 100.0, max_overdraft=-50.0)
    
    def test_properties(self):
        """Тест всех свойств класса"""
        # Тест доступного баланса (уникальная проверка)
        self.assertEqual(self.account.available_balance, 1500.0)  # 1000 + 500
        
        # Тест статуса активности
        self.assertTrue(self.account.is_active)
    
    def test_deposit_success(self):
        """Тест успешного пополнения"""
        result = self.account.deposit(200.0, "Salary")
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1200.0)
        self.assertEqual(len(self.account.transaction_history), 2)
        self.assertEqual(self.account.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account.transaction_history[-1]["amount"], 200.0)
    
    def test_deposit_negative_amount(self):
        """Тест пополнения отрицательной суммой"""
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)
    
    def test_deposit_zero_amount(self):
        """Тест пополнения нулевой суммой"""
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
    
    def test_deposit_inactive_account(self):
        """Тест пополнения заблокированного счета"""
        self.account.freeze_account()
        with self.assertRaises(ValueError):
            self.account.deposit(100.0)
    
    def test_withdraw_success(self):
        """Тест успешного снятия средств"""
        result = self.account.withdraw(200.0, "Purchase")
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(len(self.account.transaction_history), 2)
        self.assertEqual(self.account.transaction_history[-1]["type"], "WITHDRAWAL")
        self.assertEqual(self.account.transaction_history[-1]["amount"], -200.0)
    
    def test_withdraw_negative_amount(self):
        """Тест снятия отрицательной суммы"""
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)
    
    def test_withdraw_zero_amount(self):
        """Тест снятия нулевой суммы"""
        with self.assertRaises(ValueError):
            self.account.withdraw(0.0)
    
    def test_withdraw_insufficient_funds(self):
        """Тест снятия при недостатке средств"""
        with self.assertRaises(ValueError):
            self.account.withdraw(2000.0)  # Больше доступного баланса
    
    def test_withdraw_with_overdraft(self):
        """Тест снятия с использованием овердрафта"""
        result = self.account.withdraw(1200.0)  # 1000 + 500 овердрафт
        self.assertTrue(result)
        self.assertEqual(self.account.balance, -200.0)
    
    def test_withdraw_inactive_account(self):
        """Тест снятия с заблокированного счета"""
        self.account.freeze_account()
        with self.assertRaises(ValueError):
            self.account.withdraw(100.0)
    
    def test_transfer_success(self):
        """Тест успешного перевода"""
        target_account = BankAccount("999999999", 0.0, "Target User")
        result = self.account.transfer_to(target_account, 300.0, "Payment")
        
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(target_account.balance, 300.0)
        self.assertEqual(len(self.account.transaction_history), 2)
        self.assertEqual(len(target_account.transaction_history), 2)
    
    def test_transfer_negative_amount(self):
        """Тест перевода отрицательной суммы"""
        target_account = BankAccount("999999999", 0.0, "Target User")
        with self.assertRaises(ValueError):
            self.account.transfer_to(target_account, -100.0)
    
    def test_transfer_zero_amount(self):
        """Тест перевода нулевой суммы"""
        target_account = BankAccount("999999999", 0.0, "Target User")
        with self.assertRaises(ValueError):
            self.account.transfer_to(target_account, 0.0)
    
    def test_transfer_from_inactive_account(self):
        """Тест перевода с заблокированного счета"""
        target_account = BankAccount("999999999", 0.0, "Target User")
        self.account.freeze_account()
        with self.assertRaises(ValueError):
            self.account.transfer_to(target_account, 100.0)
    
    def test_transfer_to_inactive_account(self):
        """Тест перевода на заблокированный счет"""
        target_account = BankAccount("999999999", 0.0, "Target User")
        target_account.freeze_account()
        with self.assertRaises(ValueError):
            self.account.transfer_to(target_account, 100.0)
    
    def test_get_balance_statement(self):
        """Тест получения выписки по счету"""
        statement = self.account.get_balance_statement()
        
        self.assertEqual(statement["account_number"], "123456789")
        self.assertEqual(statement["account_holder"], "John Doe")
        self.assertEqual(statement["current_balance"], 1000.0)
        self.assertEqual(statement["available_balance"], 1500.0)
        self.assertEqual(statement["max_overdraft"], 500.0)
        self.assertTrue(statement["is_active"])
        self.assertEqual(statement["total_transactions"], 1)
        self.assertIsNotNone(statement["last_transaction"])
    
    def test_freeze_account_success(self):
        """Тест успешной блокировки счета"""
        result = self.account.freeze_account()
        self.assertTrue(result)
        self.assertFalse(self.account.is_active)
        self.assertEqual(len(self.account.transaction_history), 2)
        self.assertEqual(self.account.transaction_history[-1]["type"], "FREEZE")
    
    def test_freeze_already_frozen_account(self):
        """Тест блокировки уже заблокированного счета"""
        self.account.freeze_account()
        result = self.account.freeze_account()
        self.assertFalse(result)
    
    def test_unfreeze_account_success(self):
        """Тест успешной разблокировки счета"""
        self.account.freeze_account()
        result = self.account.unfreeze_account()
        self.assertTrue(result)
        self.assertTrue(self.account.is_active)
        self.assertEqual(len(self.account.transaction_history), 3)
        self.assertEqual(self.account.transaction_history[-1]["type"], "UNFREEZE")
    
    def test_unfreeze_active_account(self):
        """Тест разблокировки активного счета"""
        result = self.account.unfreeze_account()
        self.assertFalse(result)
    
    def test_set_max_overdraft_success(self):
        """Тест успешной установки лимита овердрафта"""
        result = self.account.set_max_overdraft(1000.0)
        self.assertTrue(result)
        self.assertEqual(self.account.available_balance, 2000.0)  # 1000 + 1000
        self.assertEqual(len(self.account.transaction_history), 2)
        self.assertEqual(self.account.transaction_history[-1]["type"], "OVERDRAFT_CHANGE")
    
    def test_set_negative_overdraft(self):
        """Тест установки отрицательного лимита овердрафта"""
        with self.assertRaises(ValueError):
            self.account.set_max_overdraft(-100.0)
    
    def test_get_transactions_by_type(self):
        """Тест получения транзакций по типу"""
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.account.deposit(200.0)
        
        deposits = self.account.get_transactions_by_type("DEPOSIT")
        withdrawals = self.account.get_transactions_by_type("WITHDRAWAL")
        
        self.assertEqual(len(deposits), 2)
        self.assertEqual(len(withdrawals), 1)
        self.assertEqual(deposits[0]["amount"], 100.0)
        self.assertEqual(withdrawals[0]["amount"], -50.0)
    
    def test_get_transactions_in_range(self):
        """Тест получения транзакций за период"""
        # Создаю новый счет для чистого теста
        test_account = BankAccount("TEST123", 0.0, "Test User", 0.0)
        
        # Добавляю задержку для создания разных временных меток
        import time
        time.sleep(0.01)
        
        start_time = datetime.now()
        test_account.deposit(100.0)
        time.sleep(0.01)
        
        mid_time = datetime.now()
        test_account.withdraw(50.0)
        time.sleep(0.01)
        
        end_time = datetime.now()
        test_account.deposit(200.0)
        
        # Получаю транзакции за средний период
        mid_transactions = test_account.get_transactions_in_range(start_time, mid_time)
        self.assertGreaterEqual(len(mid_transactions), 1)  # минимум deposit
        
        # Получаю все транзакции
        all_transactions = test_account.get_transactions_in_range(start_time, end_time)
        self.assertGreaterEqual(len(all_transactions), 3)  # минимум deposit + withdrawal + deposit
    
    def test_transaction_history_immutability(self):
        """Тест неизменяемости истории транзакций"""
        history = self.account.transaction_history
        original_length = len(history)
        
        # Попытка изменить историю не должна влиять на оригинал
        history.append({"fake": "transaction"})
        self.assertEqual(len(self.account.transaction_history), original_length)
    
    def test_complex_scenario(self):
        """Тест сложного сценария использования"""
        # Создаю два счета
        account1 = BankAccount("ACC001", 1000.0, "User1", 200.0)
        account2 = BankAccount("ACC002", 500.0, "User2", 100.0)
        
        # Выполню серию операций
        account1.deposit(300.0, "Salary")
        account1.withdraw(150.0, "Rent")
        account1.transfer_to(account2, 200.0, "Payment")
        account1.freeze_account()
        
        # Проверяю финальные состояния
        self.assertEqual(account1.balance, 950.0)  # 1000 + 300 - 150 - 200
        self.assertEqual(account2.balance, 700.0)  # 500 + 200
        self.assertFalse(account1.is_active)
        self.assertTrue(account2.is_active)
        
        # Проверяю историю транзакций
        self.assertEqual(len(account1.transaction_history), 5)  # INITIAL + 4 операции
        self.assertEqual(len(account2.transaction_history), 2)  # INITIAL + transfer
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Тест счета с нулевым балансом и овердрафтом
        zero_account = BankAccount("ZERO", 0.0, "Zero User", 0.0)
        self.assertEqual(zero_account.available_balance, 0.0)
        
        # Попытка снятия с нулевого счета
        with self.assertRaises(ValueError):
            zero_account.withdraw(1.0)
        
        # Тест максимального овердрафта
        zero_account.set_max_overdraft(100.0)
        zero_account.withdraw(50.0)
        self.assertEqual(zero_account.balance, -50.0)
        
        # Попытка превысить лимит овердрафта
        with self.assertRaises(ValueError):
            zero_account.withdraw(60.0)
    
    # ========== ТЕСТЫ С МОКАМИ (Классическая школа тестирования) ==========
    
    @patch('bank_account.datetime')
    def test_deposit_with_mocked_datetime(self, mock_datetime):
        """Тест пополнения с моком datetime"""
        mock_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        
        account = BankAccount("MOCK001", 100.0, "Mock User", 0.0)
        
        result = account.deposit(50.0, "Mocked deposit")
        
        self.assertTrue(result)
        self.assertEqual(account.balance, 150.0)
        
        mock_datetime.now.assert_called()
        
        transaction = account.transaction_history[-1]
        self.assertEqual(transaction["timestamp"], mock_now)
        self.assertEqual(transaction["type"], "DEPOSIT")
        self.assertEqual(transaction["amount"], 50.0)
    
    def test_transfer_with_mocked_account(self):
        """Тест перевода с моком целевого счета"""
        source_account = BankAccount("SOURCE", 1000.0, "Source User", 0.0)
        
        mock_target = Mock()
        mock_target.account_number = "TARGET"
        mock_target._is_active = True
        mock_target.deposit = Mock(return_value=True)
        
        result = source_account.transfer_to(mock_target, 200.0, "Mocked transfer")
        
        self.assertTrue(result)
        self.assertEqual(source_account.balance, 800.0)
        
        mock_target.deposit.assert_called_once_with(200.0, "Transfer from SOURCE")
        
        transfer_transaction = source_account.transaction_history[-1]
        self.assertEqual(transfer_transaction["type"], "WITHDRAWAL")
        self.assertEqual(transfer_transaction["amount"], -200.0)
        self.assertIn("Transfer to TARGET", transfer_transaction["description"])
    
    @patch('bank_account.BankAccount._add_transaction')
    def test_withdraw_with_mocked_transaction_logging(self, mock_add_transaction):
        """Тест снятия с моком логирования транзакций"""
        account = BankAccount("MOCK003", 500.0, "Mock User", 100.0)
        
        result = account.withdraw(200.0, "Mocked withdrawal")
        
        self.assertTrue(result)
        self.assertEqual(account.balance, 300.0)
        
        mock_add_transaction.assert_called_with("WITHDRAWAL", -200.0, "Mocked withdrawal")
    
    def test_get_balance_statement_with_mocked_last_transaction(self):
        """Тест получения выписки с моком последней транзакции"""
        account = BankAccount("MOCK004", 300.0, "Mock User", 50.0)
        
        mock_date = datetime(2024, 1, 1, 15, 30, 0)
        account._last_transaction_date = mock_date
        
        statement = account.get_balance_statement()
        
        self.assertEqual(statement["account_number"], "MOCK004")
        self.assertEqual(statement["current_balance"], 300.0)
        self.assertEqual(statement["available_balance"], 350.0)
        self.assertEqual(statement["last_transaction"], mock_date.isoformat())
        self.assertTrue(statement["is_active"])
    
if __name__ == '__main__':
    unittest.main()
