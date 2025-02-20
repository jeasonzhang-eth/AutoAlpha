from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CurrencyRate, CurrencyLatestRate
import datetime
import logging
import time
from functools import wraps


def timeit(func):
    """计时装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        print(f"Function {func.__name__} executed in {elapsed:.4f} seconds")
        logging.info(f"Function {func.__name__} executed in {elapsed:.4f} seconds")
        return result

    return wrapper


class DatabaseManager:
    def __init__(self, db_url="sqlite:///currency_rates.db"):
        # 创建数据库引擎，启用连接池和预编译语句
        self.engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={"timeout": 30}
        )

        # 创建所有在 Base 中定义的数据表（如果它们还不存在）
        Base.metadata.create_all(self.engine)

        # 创建一个会话工厂，用于后续创建数据库会话
        self.Session = sessionmaker(bind=self.engine)

    @timeit
    def save_rates(self, rates: dict, currency_type: str):
        """
        保存汇率数据到数据库
        :param rates: 汇率字典
        :param currency_type: 货币类型 ('fiat' or 'crypto')
        """
        try:
            session = self.Session()
            timestamp = datetime.datetime.now(datetime.timezone.utc)

            # 只清空当前货币类型的最新汇率数据
            session.query(CurrencyLatestRate).filter(
                CurrencyLatestRate.currency_type == currency_type
            ).delete()

            # 使用批量插入优化性能
            rate_records = []
            latest_rate_records = []
            for currency_code, rate in rates.items():
                price = 0 if rate == 0 else 1 / rate
                rate_data = {
                    'currency_code': currency_code,
                    'rate': rate,
                    'price': price,
                    'currency_type': currency_type,
                    'timestamp': timestamp
                }
                rate_records.append(rate_data)
                latest_rate_records.append(rate_data)

            # 批量插入历史数据
            session.bulk_insert_mappings(CurrencyRate, rate_records)
            # 批量插入最新数据
            session.bulk_insert_mappings(CurrencyLatestRate, latest_rate_records)
            session.commit()
        except Exception as e:
            logging.error(f"Error saving rates to database: {e}")
            session.rollback()
        finally:
            session.close()

    @timeit
    def get_latest_rates(self, currency_type=None):
        """
        获取最新汇率数据
        :param currency_type: 可选，指定获取特定类型的货币汇率
        :return: 包含最新汇率的字典
        """
        try:
            session = self.Session()

            # 直接从最新汇率表获取数据
            query = session.query(
                CurrencyLatestRate.currency_code,
                CurrencyLatestRate.rate
            )

            if currency_type is not None:
                query = query.filter(CurrencyLatestRate.currency_type == currency_type)

            results = query.all()

            return {record.currency_code: record.rate for record in results}
        except Exception as e:
            logging.error(f"Error fetching rates from database: {e}")
            return {}
        finally:
            session.close()

    @timeit
    def get_historical_rates(self, currency_code, start_date=None, end_date=None, limit=10000):
        """
        获取历史汇率数据
        :param currency_code: 货币代码
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param limit: 最大返回记录数
        :return: 历史汇率记录列表
        """
        try:
            session = self.Session()
            query = session.query(CurrencyRate).filter(
                CurrencyRate.currency_code == currency_code
            )

            if start_date:
                query = query.filter(CurrencyRate.timestamp >= start_date)
            if end_date:
                query = query.filter(CurrencyRate.timestamp <= end_date)

            return query.order_by(CurrencyRate.timestamp.desc()).limit(limit).all()
        except Exception as e:
            logging.error(f"Error fetching historical rates: {e}")
            return []
        finally:
            session.close()
