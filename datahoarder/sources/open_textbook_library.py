from datahoarder.source_helpers import *


def run(args):
    files = {}

    requests.packages.urllib3.disable_warnings()
    otl_url = 'https://open.umn.edu/opentextbooks/'

    otl = BeautifulSoup(requests.get('https://open.umn.edu/opentextbooks/subjects', verify=False).text, 'lxml')
    subjects = otl.select('a')
    subject_urls = []
    known_links = []

    for subject in subjects:
        href = subject.get('href')

        # This a subject site, find all books
        if '/opentextbooks/subjects/' in href:
            subject_urls.append(urljoin(otl_url, href))

    for subject in subject_urls:
        subject_page = BeautifulSoup(requests.get(subject, verify=False).text, 'lxml')
        books = subject_page.select('a')

        for book_link in books:
            if book_link.get('href') is None:

                pass

            elif '/opentextbooks/textbooks/' in book_link.get('href'):
                book_page = BeautifulSoup(
                    requests.get(
                        urljoin(otl_url, book_link.get('href')), verify=False
                    ).text,
                'lxml')
                pdf_link = book_page.find('ul', class_='BookTypes').find_all('a')


                for btn in pdf_link:
                    pdf_href = btn.get('href').split('?')[0].replace('%20', ' ')

                    if 'pdf' in pdf_href and pdf_href not in known_links:
                        cat = subject.split('/')[-1].replace('-', ' ').title()
                        print('[OPEN TEXTBOOK LIBRARY] Found file {}'.format(pdf_href))

                        if cat not in files:
                            files[cat] = [pdf_href]

                        else:
                            files[cat].append(pdf_href)

                        known_links.append(pdf_href)


    return [
        files,
        info()['meta']['friendly_name']
    ]


def info():
    return {
        'meta': {
            'id': 'open_textbook_library',
            'friendly_name': 'Open Textbook Library',
            'short_description': 'Downloads all PDF textbooks from the free website Open Textbook Library',
            'category': 'academia'
        },
        'args': {

        }
    }
