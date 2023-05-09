#importing the packages we will use
import os
import sys
import re
import itertools
#set a variable for using in while loop
print("""---Hello there.This application detect the Single nucleotide polymorphism.
It accepts VCF files as an input of the Father,Mother,son.
After our marvellous and magical calculations,we output whether it is their son or not.
for example the application detected that salma is my daughter.\n\n\n  """)
#this while loop is for the repetition
while True:
    #created a directory variable
    dir=os.listdir()
    print(dir)
    #created Names variable to store the parents names and an empty list
    Names=["Father","Mother","Son"]
    list=[]
    #we made a nested for-while loop to take the inputs from the user
    for i in Names:
        while True:
            #set a variable to contain the input from user
            v=input("Please input the "+str(i)+" VCF file: ")
            #set an if statement to detect that the file is in vcf format and in the directory
            if v.endswith("vcf")==True and v in dir:
                list.append(v)
                break
            #else statement to make the user reenter the file name in vcf file
            else:
                print("The file has invalid format or not in the directory\nPlease enter the file in .vcf format and put it with the script in the same directory")
                continue
    #set a list contaimig the 3 variables containing file names
    #set an emty lists to contain future lists
    son=[]
    father=[]
    mother=[]

    #here we iterate over file names to open them
    for i in list:
        k=open(i).readlines()
        #here we iterate over each file and remove all the info in it leaving the SNPS only
        for l in k:
            #list to contain the edited file content
            newvcf=[]
            # here we removed the extra sentences at the beginning of the file
            if not l.startswith('#'):
                newvcf.append(l)
                #here we iterate over the newly edited content and takes the Chrom-Pos-Alt only
                for w in newvcf:
                    #we split the file by tab making each line in separate list
                    p=re.split("\t|\s",w)
                    #if statements to append the newly edited lists (chrom,pos,alt) to the respected lists above
                    if i==list[0]:
                        father.append(([p[0],p[1],p[4]]))
                    if i==list[1]:
                        mother.append(([p[0],p[1],p[4]]))
                    if i==list[2]:
                        son.append(([p[0],p[1],p[4]]))
    #set a counting variables
    father_count=len(father)
    mother_count=len(mother)
    son_count=len(son)
    son_father=[]
    mother_son=[]
    father_mother_son=[]
    father_diff=[]
    mother_diff=[]

    #used here zip from itertools package to iterate over the 3 lists at the same time
    for i,j,k in zip(son,father,mother):
        #if statements for the comparison adding the each similar SNP to the designated lists
        if i==j and not i==k==j:
            #these set of codes was written to avoid repetition
            if i not in son_father:
                son_father.append(i)
        if i==k and not i==j==k:
            if i not in mother_son:
               mother_son.append(i)
        if i==j==k:
            if i not in father_mother_son:
                father_mother_son.append(i)
    #for loop to extract the differences
    for i in son:
        if i not in father and i not in father_diff:
           father_diff.append(i)
        if i not in mother and i not in mother_diff:
            mother_diff.append(i)
    #here we calcualted the percentage of the similarity
    percentage=round((len(son_father)+len(mother_son)+len(father_mother_son))/max(son_count,father_count,mother_count)*100,1)
    if percentage >=80:
        print("\n\nThis child belongs to these parents\nThe percentage of similarity was "+str(percentage)+"\n\n\n")
    if percentage <80:
        print("\n\n This is not their child\nThe percentage of similarity was "+str(percentage)+"\n\n\n")
    #we created a variable to contain the father-mother differences lists and a variable to contain the names of the future file object
    differences=[father_diff,mother_diff]
    filename=['father_diff.txt','mother_diff.txt']
    #here we made a choice for the user if he wants the differences in seperate file
    while True:
        e=input("If you need to save the difference positions in file,please input 'Y' otherwise input 'N': ").upper()
        if e=='Y':
            #in the two set of codes below if there are no diff it will print it and remove it from differences
            if len(father_diff)==0:
                print('There are no differences between son and father')
                differences.remove(father_diff)
                filename.remove('father_diff.txt')
            if len(mother_diff)==0:
                print('There are no differences between son and mother')
                differences.remove(mother_diff)
                filename.remove('mother_diff.txt')
            #nested for loop to create files and append the differences to it
            for i in range(len(filename)):
                #here file will be father diff and mother diff according to file name variable
                file=open(str(filename[i]),'w')
                file.write('["chrom","POS","Alt"]\n')
                snps=differences[i]
                #for loop for the appending
                for j in snps:
                    file.write(str(j)+"\n")
                file.close()
                #nested while loop user choice if he wants to rename each file
                while True:
                    rename=input("Do you wish to rename the "+filename[i] +' file ?!\nPlease note that the file name now is '+filename[i]+"\nit is advised to rename if you will make additional runs\n'Y'/'N':").upper()
                    if rename=='Y':
                        #for loop was made for the rename of the file
                        for b in filename:
                            while True:
                                a=input("please input your desired name for " + filename[i]+ ':')
                                #this was made to detect if the inputted name wasnt already in the directory
                                if a in dir:
                                    print("The directory has similar file name\nPlease enter another name")
                                    continue
                                #if everything is good , the rename function is excuted
                                else:
                                    os.rename(str(filename[i]),a)
                                    break
                            break
                        break
                    #if the answer is no it will skip all of these
                    elif rename=='N':
                        break
                    else:
                        print("Your input is invalid")
                        continue
            break
        #if the user dont want written files it will skip all of the above
        elif e=='N':
            break
        else:
            print("Your input is invalid")
            continue
    #while loop for user choice if he want to input another files
    while True:
        repeat=input('Do you want to try another files ?\n"Y" or "N"').upper()
        #if yes it will break this loop and will return to the first while loop which is the program by continue below
        if repeat=='Y':
            break
        #if the answer N it will close the file with a farewell message
        elif repeat=='N':
            sys.exit("Thank you for using our application.ばかり, use contraceptives in the future so salma won't be your daughter")
        #here the loop will be repeated if the input is incorrect
        else:
            print("Your input is invalid")
            continue
    continue
