import time # importing time ()
class SortAnimal:  # creating a class.

    def __init__(self, dummy_data):       # declaring class variables
        self.dummy_data = dummy_data
        self.combined_len=len(dummy_data)
        self.dummy_data_copy = dummy_data.copy()
        self.ewes_room = []
        self.lambs_room = []

        #print(f"Animals are: {self.dummy_data}") # if needed for test.

    # method for ewes
    def sort_ewes(self, ele):
        time.sleep(0.5)
        self.ewes_room.append(ele)
        print(f"{ele} successfully sended to ewes room")
        print('*'*25)
        self.dummy_data.remove(ele)

    # method for lamb
    def sort_lamb(self, ele):
        time.sleep(0.5)
        self.lambs_room.append(ele)
        print(f"{ele} successfully sended to lambs room")
        print('*'*25)
        self.dummy_data.remove(ele)

    # method for calling the right method based on condition... this is internally calling 4 functions...
    def call_sorting_man(self):
        for ele in self.dummy_data_copy:
            print(f"sending {ele} to it's room.")
            if ele[-3:] == 'red' and ele[0:4] == 'ewes':
                self.sort_ewes(ele)                            # calling function based on condition.

            elif ele[-5:] == 'green' and ele[0:4] == 'lamb':
                self.sort_lamb(ele)                            # calling function based on condition.

            else:
                print(f"{ele} wrong animal KILL IT!")

        del self.dummy_data_copy
        print(f"Generating Report:")
        self.get_data()                                      # calling function for basic details 

    def get_data(self):
        print(f"Total animals outside: {self.combined_len}")
        print(f"Total animal in ewes room: {len(self.ewes_room)}")
        print(f"Total animal in lamb room: {len(self.lambs_room)}")
        if self.combined_len == len(self.ewes_room) + len(self.lambs_room):
            print(f"All {self.combined_len} animals reached in their rooms")
        else:
            print(f"{len(self.dummy_data)} animals missing.")
        print(f"{len(self.dummy_data)} animals outside.")

dummy_data = ['ewes1_red', 'ewes2_red', 'lamb1_green', 'ewes_3_red', 'lamb2_green', 'ewes_4_red', 'lamb3_green', 'lamb4_green', 'lamb5_green',
                  'ewes_5_red', 'ewes_6_red', 'ewes_7_red', 'ewes_8_red']

animal_sorter = SortAnimal(dummy_data)
animal_sorter.call_sorting_man()