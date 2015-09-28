import sys
import rethinkdb as r

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: compute_table_metrics.py <tablename>", file=sys.stderr)
        exit(-1)
    RDB_HOST =  os.environ.get('RDB_HOST')
    RDB_PORT = os.environ.get('RDB_PORT')
    RDB_DB = "SerIoTics"
    RDB_TABLE = sys.argv[1:]

    def createNewConnection():
        return r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    def getStartTime():
    	return r.table(RDB_TABLE).filter(r.row('count').gt(0)).min('time')
    def getStopTime():
    	return r.table(RDB_TABLE).filter(r.row('count').gt(0)).max('time')
    def getRecordCount():
    	return r.table(RDB_TABLE).filter(r.row('count').gt(0)).sum('count')
    def computeRecordsPerSecond(start_time, end_time, num_records):
    	return (end_time-start_time)/num_records

	connection = createNewConnection()
    print(computeRecordsPerSecond())
    connection.close()