import greenview, os.path, logging
from greenview.examples import maintain

def main(root):
    logFile = os.path.join(root, 'update.log')
    logging.basicConfig(filename=logFile, level=logging.INFO, format='%(levelname)s: %(asctime)s %(message)s')
    logging.info('Started')
    try:
        for meter_id in [213, 69, 111, 15, 490]:
            maintain(root, meter_id)
    except greenview.ServerError, e:
        logging.error(e.message)
    except Exception, e:
        logging.error('<--------------Unexpected error--------------')
        logging.error(e.message)
    logging.info('Finished')
    
if __name__ == "__main__":    
    root = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(root): os.makedirs(root)
    main(root)
