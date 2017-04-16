import csv
import json
import xlrd
import os

class csvJSON:
    def correctDataType(self,item):
        remove_dollar = item
        try:
            remove_dollar = item.replace("$", "")
        except AttributeError:
            pass
        #print(remove_dollar)
        if remove_dollar == '':
            return None
        else:
            try:
            	return int(remove_dollar)
            except ValueError:
                pass

            try:
                return float(remove_dollar)
            except ValueError:
                pass
        
        return item

    def addModifier(self, title, data, modifier_counter, row, row_index):
        #potentially add in modifier counter parameter to keep track
        #and parameter of where to add from row index 
        #get number and param name
        #global modifier_counter
        modifier_title = title.split('_')
        modifier_index = modifier_title[1]
        modifier_attribute = modifier_title[2]

        #if modifier_index == modifier counter
        if int(modifier_index) == modifier_counter:
            #print('counter %d' % modifier_counter) #add to existing dictionary data[counter]
            data[modifier_counter-1].update({modifier_attribute : self.correctDataType(row[row_index])})
            return 0
        else:
        	#make new dictionary for modifier attribute : row[i]
        	data.append({modifier_attribute : self.correctDataType(row[row_index])})
        	#modifier_counter+=1
        	#somehow add row[i] to current 
        #data
        #print('Index: %d Attribute: %s ' % (int(modifier_index), modifier_attribute))
        return 1

    def toJSON(self, row):
        i = 0
        modifier_counter = 0
        data = {} 
        data['modifiers'] = []
        for title in self.pop:
            if 'modifier' in title: #if modifier else normal
                try:
                     modifier_counter += self.addModifier(title, data['modifiers'], modifier_counter, row, i)
                except IndexError:
                    #print('empty slot')
                    pass
            else:    	
                try:
                    data[title] = self.correctDataType(row[i])
                except IndexError:
                    data[title] = None

            i+=1
        self.mylist.append(data)

    # read stocks data, print status messages
    def __init__(self,filePath, fileType):
        #if type == xlsx
        #fileType = '.xlsx'
        if fileType == '.xlsx':
            workbook = xlrd.open_workbook(filePath)
            self.mylist = []
            #for each sheet in 
            for sheet in workbook.sheets():
                #self.worksheet = workbook.sheet_by_name('Sheet1')
                self.worksheet = sheet
                self.pop = self.worksheet.row_values(0)

                for rownum in range(self.worksheet.nrows)[1:]:
                    #to 
                    #print(self.worksheet.row_values(rownum))
                    self.toJSON(self.worksheet.row_values(rownum))
                    #set stocks and pop

        #add else statement here
        else:
            self.stocks = csv.reader(open(filePath, 'rb'))
            self.pop = next(self.stocks) #get the column headings
            self.mylist = [] #to place json in
            for line in self.stocks:
                self.toJSON(line) #row to json
        newfilename =  '%s.json' % os.path.splitext(os.path.basename(filePath))[0]
        with open(newfilename, 'w') as outfile:  
            json.dump(self.mylist, outfile, indent=4, sort_keys=True) #dump to json and sort alphabetically



