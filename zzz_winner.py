from selenium import webdriver
from time import sleep

from selenium.webdriver.chrome.options import Options


CHROME_DRIVER_PATH = ''
verbose = True
headless = False


class ZZZPlayer:
    def __init__(self):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)

        self.driver.get('http://zzzscore.com/1to50/en/')
        self.driver.execute_script("window.scrollTo(0, 120)")

        self.cells = {}  # Reference to cells -> number of cell : cell
        self.positions = {}  # Cell of the target number -> targer number : number of cell
        self.to_discover = 1

        self.load_numbers()

    def load_numbers(self):
        """
        Load the first 25 numbers in memory and save the references of the cells
        """
        for i in range(1, 26):
            elem = self.driver.find_element_by_css_selector(f'div:nth-child({i}) > .box')
            parent = elem.find_element_by_xpath('..')  # Reference to cell
            self.cells[i] = parent  # Assing the refence of the cell to the cell number
            self.positions[int(self.cells[i].text)] = i  # Assign the target number to the number of cell

    def next_click(self, target_number):
        """
        Get the cell which contain the target number. If is not in memory, will look for it in order of previous clicks
        :param target_number: Number searched for.
        :return: Reference to the cell.
        """
        if target_number in self.positions:
            return self.positions[target_number]
        else:
            value_of_cell = ''
            while str(target_number) != value_of_cell:
                value_of_cell = ''
                cell_to_discover = int(self.positions[self.to_discover])
                while value_of_cell == '':
                    value_of_cell = self.cells[cell_to_discover].text
                if verbose:
                    print(f'\tDiscovered value {value_of_cell} in cell {cell_to_discover}')
                self.positions[int(value_of_cell)] = cell_to_discover
                self.to_discover += 1
            return self.positions[int(value_of_cell)]

    def play(self):
        if verbose:
            print('\nStarting...')
        for i in range(1, 51):
            cell_to_click = self.next_click(i)
            if verbose:
                print(f'Value {i} is in the cell {cell_to_click}')
            self.cells[cell_to_click].click()

        sleep(.2)  # At this point, the game has ended. Wait until the time loads
        result = self.driver.find_element_by_id('time').text
        if verbose:
            print('Finshed in', result, 'seconds.')

        self.driver.quit()
        return float(result)


if __name__ == '__main__':
    player = ZZZPlayer()
    player.play()
