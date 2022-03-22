from apscheduler.schedulers.background import BackgroundScheduler
#from backend.scraping.scraping import scraping
from backend.ml.ml import proprocessing
def batch():
    print('バッチ開始')
    proprocessing()
    print('完了')
sched = BackgroundScheduler(standalone=True,coalesce=True)
sched.add_job(batch, 'interval', minutes=1)
sched.start()