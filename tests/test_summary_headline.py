import country_code_run
import pytest
import json
import datetime
import os
import re
import logging

logging.basicConfig(level=logging.INFO, filename=os.path.dirname(os.path.abspath('country_code_run.py'))
                                                 + '/logs/test_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                                                 + '.txt',
                    format='%(process)d--%(asctime)s--%(levelname)s--%(message)s')


def test_attr_segments_summary_headline():
    data_segment_summary_headline = country_code_run.read_json_file()['data']['attributes']['segments'][0]['summary'][
        'headline']
    reSpecialCharacter = re.compile('[@_!#$%^&*<>?/}{~:]')
    check_for_special_character = reSpecialCharacter.search(data_segment_summary_headline)
    assert check_for_special_character is None


def test_attr_summary_headlines():
    data_attr_summary_headlines = country_code_run.read_json_file()['data']['attributes']['summary']
    for i in range(len(data_attr_summary_headlines)):
        reSpecialCharacter = re.compile('[@_!#$%^&*<>?|}{~:]')
        check_for_special_character = reSpecialCharacter.search(str(data_attr_summary_headlines[i]['headline']))
        assert check_for_special_character is None
