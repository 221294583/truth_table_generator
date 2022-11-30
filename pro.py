import copy
import re

class pro:
    def __init__(self,ini):
        self.letters=[]
        self.operators=['(',')','and','not','or','then','equal']
        self.temp=list(filter(None, re.split(r'[\s+]|(\W)', ini)))
        self.length=len(self.temp)
        self.table_cases=[[]]
        self.brackets=[]
        self.result=[]

        for i in range(self.length):
            self.brackets.append(0)

        for i in self.temp:
            if i not in self.operators and i not in self.letters:
                self.letters.append(i)

    def table_base(self):
        for i in range(len(self.letters)):
            self.table_cases=self.generate_case(self.table_cases)
        self.table_cases=self.reverse(self.table_cases)

    def generate_case(self,last):
        temp_before=copy.deepcopy(last)
        temp_after =copy.deepcopy(last)
        for i in range(len(temp_before)):
            temp_before[i].append(0)
        for i in range(len(temp_after)):
            temp_after[i].append(1)
        result=temp_before+temp_after
        return result

    def reverse(self,l):
        temp=l
        for i in range(len(temp)):
            temp[i]=temp[i][::-1]
            for j in range(len(temp[i])):
                if temp[i][j]==1:
                    temp[i][j]=True
                else:
                    temp[i][j]=False
        return temp

    def bracket(self):
        count=0
        l=[0]
        last=-1
        for i in range(self.length):
            if self.temp[i]==self.operators[0]:
                count+=1
                l.append(count)
                self.brackets[i]=count
            elif self.temp[i]==self.operators[1]:
                self.brackets[i]=l[len(l)+last]
                l.remove(l[len(l)+last])

    def iterate(self):
        self.result=[]
        for i in self.table_cases:
            self.result.append(self.cal(self.temp,self.brackets,i))

    def cal(self,instruction,brackets_mapping,truth_case):
        #print('cal called',instruction,truth_case)
        ans = None
        i = 0
        if instruction[0]=='(':
            ending_mark = brackets_mapping[i]
            ending_index = brackets_mapping.index(ending_mark,1)
            ans=self.cal(instruction[1:ending_index],brackets_mapping[1:ending_index],truth_case)
            i=ending_index
        elif instruction[0] not in self.operators:
            ans=truth_case[self.letters.index(instruction[0])]
            i+=1
        elif instruction[0]=='not':
            if instruction[1]=='(':
                ending_mark = brackets_mapping[1]
                ending_index = brackets_mapping.index(ending_mark, 2)
                ans = self.cal_not(self.cal(instruction[2:ending_index], brackets_mapping[2:ending_index], truth_case))
                i = ending_index
            elif instruction[1] not in self.operators:
                ans=self.cal_not(truth_case[self.letters.index(instruction[1])])
                i+=2

        while i < len(instruction):
            ##print(i,instruction[i])
            operator = instruction[i]
            if operator in self.operators:
                if operator=='and':
                    if instruction[i+1]=='(':
                        ending_mark = brackets_mapping[i+1]
                        ending_index = brackets_mapping.index(ending_mark, i + 2)
                        #print(ending_mark,ending_index)
                        ans = self.cal_and(ans,self.cal(instruction[i + 2:ending_index], brackets_mapping[i + 2: ending_index],
                                       truth_case))
                        i=ending_index
                    elif instruction[i+1] not in self.operators:
                        ans=self.cal_and(ans,truth_case[self.letters.index(instruction[i+1])])
                        i+=1
                    elif instruction[i+1]=='not':
                        if instruction[i+2] == '(':
                            ending_mark = brackets_mapping[i+2]
                            ending_index = brackets_mapping.index(ending_mark, i+3)
                            ans = self.cal_and(ans,self.cal_not(
                                self.cal(instruction[i+3:ending_index], brackets_mapping[i+3:ending_index], truth_case)))
                            i = ending_index
                        elif instruction[i+2] not in self.operators:
                            ans = self.cal_and(ans,self.cal_not(truth_case[self.letters.index(instruction[i+2])]))
                            i += 2
                if operator=='or':
                    if instruction[i+1]=='(':
                        ending_mark = brackets_mapping[i+1]
                        ending_index = brackets_mapping.index(ending_mark, i + 2)
                        ans = self.cal_or(ans,self.cal(instruction[i + 2:ending_index], brackets_mapping[i + 2:ending_index],
                                       truth_case))
                        i=ending_index
                    elif instruction[i+1] not in self.operators:
                        ans=self.cal_or(ans,truth_case[self.letters.index(instruction[i+1])])
                        i+=1
                    elif instruction[i+1]=='not':
                        if instruction[i+2] == '(':
                            ending_mark = brackets_mapping[i+2]
                            ending_index = brackets_mapping.index(ending_mark, i+3)
                            ans = self.cal_or(ans,self.cal_not(
                                self.cal(instruction[i+3:ending_index], brackets_mapping[i+3:ending_index], truth_case)))
                            i = ending_index
                        elif instruction[i+2] not in self.operators:
                            ans = self.cal_or(ans,self.cal_not(truth_case[self.letters.index(instruction[i+2])]))
                            i += 2
                if operator=='then':
                    if instruction[i+1]=='(':
                        ending_mark = brackets_mapping[i+1]
                        ending_index = brackets_mapping.index(ending_mark, i + 2)
                        ans = self.cal_then(ans,self.cal(instruction[i + 2:ending_index], brackets_mapping[i + 2: ending_index],
                                       truth_case))
                        i=ending_index
                    elif instruction[i+1] not in self.operators:
                        ans=self.cal_then(ans,truth_case[self.letters.index(instruction[i+1])])
                        i+=1
                    elif instruction[i+1]=='not':
                        if instruction[i+2] == '(':
                            ending_mark = brackets_mapping[i+2]
                            ending_index = brackets_mapping.index(ending_mark, i+3)
                            ans = self.cal_then(ans,self.cal_not(
                                self.cal(instruction[i+3:ending_index], brackets_mapping[i+3:ending_index], truth_case)))
                            i = ending_index
                        elif instruction[i+2] not in self.operators:
                            ans = self.cal_then(ans,self.cal_not(truth_case[self.letters.index(instruction[i+2])]))
                            i += 2
                if operator=='equal':
                    if instruction[i+1]=='(':
                        ending_mark = brackets_mapping[i+1]
                        ending_index = brackets_mapping.index(ending_mark, i + 2)
                        ans = self.cal_equal(ans,self.cal(instruction[i + 2:ending_index], brackets_mapping[i + 2: ending_index],
                                       truth_case))
                        i=ending_index
                    elif instruction[i+1] not in self.operators:
                        ans=self.cal_equal(ans,truth_case[self.letters.index(instruction[i+1])])
                        i+=1
                    elif instruction[i+1]=='not':
                        if instruction[i+2] == '(':
                            ending_mark = brackets_mapping[i+2]
                            ending_index = brackets_mapping.index(ending_mark, i+3)
                            ans = self.cal_equal(ans,self.cal_not(
                                self.cal(instruction[i+3:ending_index], brackets_mapping[i+3:ending_index], truth_case)))
                            i = ending_index
                        elif instruction[i+2] not in self.operators:
                            ans = self.cal_equal(ans,self.cal_not(truth_case[self.letters.index(instruction[i+2])]))
                            i += 2
            i+=1
        #print('cal ended',ans)
        return ans


    def cal_and(self,a,b):
        #print('and called')
        return a and b

    def cal_or(self,a,b):
        return a or b

    def cal_not(self,a):
        return not a

    def cal_then(self,a,b):
        return False if a and not b else True

    def cal_equal(self,a,b):
        return a==b

    def print(self):
        num_row=len(self.table_cases)
        num_column=len(self.letters)+1
        print(self.result)
        first_row=list(map(lambda x:'{:^7}'.format(str(x)),self.letters))
        temp=' '.join(self.temp)
        temp='{:^{}}'.format(temp,len(temp)+6)
        first_row.append(temp)
        print(''.join(first_row))
        for i in range(num_row):
            buffer=list(map(lambda x:'{:^7}'.format(str(x)),self.table_cases[i]))
            buffer=''.join(buffer)
            buffer+='{:^{}}'.format(str(self.result[i]),len(temp)+6)
            print(buffer)
