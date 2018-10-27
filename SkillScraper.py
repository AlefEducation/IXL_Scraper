"""
This Script scrapes the skills from https://www.ixl.com/

Author: Ali Nadaf
Company: Alef Education
"""
#import libraries
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

#configs
course_link = {'Math':'math', 'Language':'ela','Science':'science'}
Skill_code, Skill_name, Skill_category, Grade_level, course_name = [], [], [], [], []

def scraper(weblink):
    for course_ in course_link:
        list_grades = []
        main_page_link = weblink + course_link[course_]
        main_page_response = requests.get(main_page_link, timeout=5)
        main_page_content = BeautifulSoup(main_page_response.content, "html.parser")
        grades_side = main_page_content.find(class_="skill-tree-aside")
        links = grades_side.find_all('a')
        for link_ in links:
            list_grades.append(link_.attrs['href'])
        for grade in list_grades:
            page_link = 'https://www.ixl.com/' + grade
            page_response = requests.get(page_link, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            skill_node = page_content.find(class_='skill-tree-body')
            Skill_node_list = skill_node.find_all('span')
            i = 0
            for skill_name in Skill_node_list:
                if i % 2 == 0:
                    Skill_code.append(skill_name.contents[0])
                    Skill_category.append(skill_name.findAllPrevious(class_='skill-tree-skills-header')[0].contents[0])
                    Grade_level.append(os.path.basename(grade))
                    course_name.append(course_)
                else:
                    Skill_name.append(skill_name.contents[0])
                i+=1
            print(' %s is scraped!' % grade)
        print('Scraping %s is complete!' %course_)
        print('-----------------------------------')
    Skill_dict = {'Skill Code': Skill_code,
                  'Skill Category': Skill_category,
                  'Grade Level': Grade_level,
                  'Course Name': course_name,
                  'Skill Name': Skill_name}
    skill_df = pd.DataFrame.from_dict(Skill_dict)
    skill_df.to_csv('IXL_Skill_List.csv', index=False)
    print('done!')

if __name__=='__main__':
    scraper(weblink = 'https://www.ixl.com/')

