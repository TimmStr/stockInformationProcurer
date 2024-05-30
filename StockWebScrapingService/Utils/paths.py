STOCK_INFORMATION_PROCURER = "stockinformationprocurer"

MONGO_PATH = "mongodb://mongodb:27017/"
MONGO_CLIENT = "stockinformations"
MONGO_DATABASE = "stocks"

POSTGRES_DATABASE = f"jdbc:postgresql://{STOCK_INFORMATION_PROCURER}-postgres-1:5432/users"

HTTP = "http://"

DOCUMENT_SERVICE = f"{HTTP}{STOCK_INFORMATION_PROCURER}-document-service-1:9010"
MAIL_SERVICE = f"{HTTP}{STOCK_INFORMATION_PROCURER}-mail-service-1:9020"
STOCK_ANALYSIS_SERVICE = f"{HTTP}{STOCK_INFORMATION_PROCURER}-stock-analysis-service-1:9030"
STOCK_WEB_SCRAPING_SERVICE = f"{HTTP}{STOCK_INFORMATION_PROCURER}-stock-web-scraping-service-1:9040"
USER_SERVICE = f"{HTTP}{STOCK_INFORMATION_PROCURER}-user-service-1:9050"

INVESTING_URL = f"{HTTP}www.investing.com/equities/"
STOCKS = f"stocks/"

CSV_EXTENSION = f".csv"