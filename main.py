import argparse,os
from crawler.xiaohang import xhrun
from threading import Thread
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',help="The name of movies",dest="name",action='store',type=str)
    parser.add_argument('-0','--output',help="The output of result",dest="output",action='store',type=str)
    args = parser.parse_args()
    if not os.path.exists("download"):
        os.mkdir("download")

    ts = [
        Thread(target=xhrun,args=(args.name,)),
    ]

    for t in ts:
        t.start()
    
    for t in ts:
        t.join()
    

if __name__ == "__main__":
    main()