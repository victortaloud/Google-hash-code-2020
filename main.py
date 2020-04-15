import sys
import datetime
import os
import os.path
import logging 
from config import *

from prompt_toolkit import prompt
import time
import datetime

from library import library
from book import book
from library_log import library_log


from book import * 
from library import * 
from library_log import * 
from Solution import * 



def _get_score_with_books_excluded(list_sorted_librairies_): 
    for librairie in list_sorted_librairies_ : 
        books = librairie.books
        total_score = 0 
        for book in books :
            total_score = total_score + int(book.score)
    return total_score

def _get_listed_librairies_in_scope_duration(deadlines_, list_sorted_librairies_) : 
    d_day = 0 
    list_sorted_librairies_on_scope = []
    # Obtenir librairie sans la dernière
    for libraire in list_sorted_librairies_ : 
        d_day = d_day + int(libraire.sign_in_duration)
        if d_day < deadlines_ : 
            list_sorted_librairies_on_scope.append(libraire)


    # Obtenir les livres de la dernière librairie
    if len(list(set(list_sorted_librairies_) - set(list_sorted_librairies_on_scope))) > 0 : 
        last_librairies_before_deadline = list(set(list_sorted_librairies_) - set(list_sorted_librairies_on_scope))[0]
        new_last_librairies_with_books_on_scope = []
        for day_lib in range(last_librairies_before_deadline.sign_in_duration,deadlines_,1) : 
            new_books_list = []
            increment = 0 
            for book in last_librairies_before_deadline.books : 
                if d_day <= deadlines_ : 
                    new_books_list.append(book)
                increment = increment + 1 
                if increment >= last_librairies_before_deadline.max_number_books : 
                    increment = 0 
                    d_day = d_day + 1 
        last_librairies_before_deadline.books = new_books_list
        list_sorted_librairies_on_scope.append(last_librairies_before_deadline)
            

    return list_sorted_librairies_on_scope


def get_score(deadlines_ , list_sorted_librairies_ ) : 
    # Exclure les livres qui sont après la deadline
    list_sorted_librairies_on_scope = get_listed_librairies_in_scope_duration(deadlines_, list_sorted_librairies_)

    # Calcul du score pour chaque librairie
    final_score = get_score_with_books_excluded(list_sorted_librairies_on_scope)

    return final_score


logging.getLogger().setLevel(logging.INFO)

# from photo import Photo
# from slide import Slide
# from slideshow import Slideshow
# from algo import *

def parse_input(filename):

    f = open(filename)

    # Get parameters
    list_books = []
    list_libraries = []
    flag = 0

    for (counter, line) in enumerate(f):
        line_splitted = line.split()
        
        if len(line_splitted) == 0:
            break
        else: 
            if counter == 0:
                nb_books = int(line_splitted[0]) # to check parsing is correct
                nb_libraries = int(line_splitted[1]) # to check parsing is correct
                nb_days = int(line_splitted[2])

            elif counter == 1:
                for book_id, book_score in enumerate(line_splitted):
                    book_item = book(
                        id = book_id,
                        score = book_score
                    )
                    list_books.append(book_item)
                    del book_item
                assert(len(list_books) == nb_books)
            
            else:
                
                if flag == 0:
                    library_item = library(
                        sign_in_duration = line_splitted[1],
                        max_number_books = line_splitted[2]
                    )

                    library_item.id = int(counter/2)

                    nb_books_in_lib = int(line_splitted[0]) # to check parsing is correct
                    flag += 1

                elif flag == 1:
                    library_item.books = []

                    for book_id_str in line_splitted:
                        book_id = int(book_id_str)
                        library_item.books.append( list_books[book_id] )

                    assert( len(library_item.books) == nb_books_in_lib)
                    flag = 0

                    list_libraries.append(library_item)
                    del library_item

                    
                else:
                    raise Exception("Parsing error: Flag greater than 1 ")
                
    f.close()
    print(f'File description: Days {nb_days} - nb_libraries {nb_libraries} - nb_books {nb_books} ')
    assert(len(list_libraries) == nb_libraries)
    return nb_days, list_libraries, list_books


def solver_v0(list_photos):
    slides = []

    for photo in list_photos:
        if photo.orientation == 'V':
            continue
        slides.append(Slide([photo]))

    slideshow = Slideshow(slides)

    return slideshow

def solver_v1(list_photos):
    print("lancement du glouton")
    #algo = Algo(list_photos)
    
    #return algo.glouton()
    return 0



def write_submission(solution, submission_name):
    # inputs = solution, submission_name

    f = open(submission_name, "w")

    # slides = slideshow.slides
    

    # f.write(str(len(slides)) + '\n')

    # for slide in slides[:-1]:
    #     line = [str(photo.id) for photo in slide.photos]
    #     line_str = ' '.join(line) + '\n'
    #     f.write(line_str)

    # # last line without \n
    # last_slide = slides[-1]
    # last_line = [str(photo.id) for photo in last_slide.photos]
    # last_line_str = ' '.join(last_line)
    last_line_str = solution
    f.write(last_line_str)
    f.close()


def get_file_to_process(file_ids):
    try:
        filepaths = [FILEPATHS[idx] for idx in  file_ids]
    except:
        raise Exception('file ids typed are not in config var FILEPATHS')
    return filepaths


def run(filenames):

    # create a folder with all the files for this submission
    path = './submissions/' + datetime.datetime.now().isoformat()
    os.mkdir(path)
    
    for filename in filenames:
        logging.info(f'{filename} processing started')

        # PARSING FUNCTIONS 
        days, list_libraries, list_books = parse_input(filename)

        print(list_libraries[0])
        
        now = datetime.datetime.now()
        logging.info(f'{filename} parsed - {now}')
        start_time = time.time()

        # solver
        # solution = solver_v1(list_photos)
        logging.info(f'{filename} solved')
        time.sleep(3) ## TO REMOVE 
        end_time = time.time()
        computing_time = datetime.timedelta(seconds=(end_time - start_time)) 

        # get score
        score = get_score(deadlines_ = days, list_sorted_librairies_ = list_libraries)
        logging.info(f'{filename} SCORE = {score} - SOLVING TIME = {computing_time}')

        # create submission name and write output file
        submission_name = path + '/Kalsita_' + filename.split('/')[-1]

        solution = 'This is a test solution'
        
        write_submission(solution, submission_name)
        logging.info(f'{filename} submission written')


if __name__ == "__main__":

    prompt_files_idx = prompt('Enter file ids to process (ex: a c b): ')
    filenames = get_file_to_process(prompt_files_idx)
    run(filenames)

    