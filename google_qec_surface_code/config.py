# config.py
import logging

def setup_logging(environment='development', log_file_name = "surface_code.log"):
    if environment == 'development':
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.StreamHandler(),  # 输出到控制台
                                logging.FileHandler(f"logs/{log_file_name}", mode='w')
                            ])
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler(f"logs/{log_file_name}", mode='a')  # 生产环境日志文件追加模式
                            ])