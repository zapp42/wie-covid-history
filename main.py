import requests
from bs4 import BeautifulSoup


def main():
    inhalt_seite = requests.get('https://www.wiesbaden.de/leben-in-wiesbaden/gesundheit/gesundheitsfoerderung/coronafallzahlen.php').content
    soup = BeautifulSoup(inhalt_seite, 'html.parser')
    data_div = soup.select_one("#SP-content > div:nth-child(4) > div:nth-child(2)")
    print(data_div)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
