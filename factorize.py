import time
import sys
import logging
import multiprocessing 
from multiprocessing import Process, Pool, current_process,Semaphore,Manager

###################   one processing   #########################

def factorize_one(*number):
    list = []

    for el in number:
        el_ = []
        for i in range(1, el + 1 ):
            if el % i == 0:
                el_.append(i)
        list.append(el_)         
    return list

###################   multi processing   #########################

def factorize_two(semaphore: Semaphore, r: list, num):
    name = current_process().name
    with semaphore:
        list = []
        for i in range(1, num + 1 ):
           if num % i == 0:
                list.append(i)
        r[name] = list
        sys.exit(0)  


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    n_cores = multiprocessing.cpu_count()

###################   one processing   #########################

    start = time.time() 
    a, b, c, d , e , j ,l , p  = factorize_one(128, 255, 99999, 10651060 , 10000000 , 10000000 , 10000000 , 10000000)
    end = time.time()
    logging.info(f"===== Time working one processing: {end - start} seconds  ======")

    print(f"{a}\n{b}\n{c}\n{d}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
  
###################   multi processing   #########################
    
    args = (128, 255, 99999, 10651060 , 10000000 , 10000000 , 10000000 , 10000000)
    
    semaphore = Semaphore(n_cores)
    start_p = time.time()

    with Manager() as m:     
        result = m.dict()
        prs = []
        for num in args:
            pr = Process(name=f'Process-{num}', target=factorize_two, args=(semaphore, result, num))
            pr.start()
            prs.append(pr)
        [pr.join() for pr in prs]
        
    end_p = time.time()
    logging.info(f"======  Time working multi processing: {end_p - start_p} seconds   ======")
    
    
    print('End program')
   

# ===== result 
# ===== Time working one processing: 2.294024705886841 seconds  
# ===== Time working multi processing: 0.8270580768585205 seconds   