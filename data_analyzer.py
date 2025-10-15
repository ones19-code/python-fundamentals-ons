import argparse
from utils import greet, add_numbers

def main():
 
   name = "Ons"
   age = 23
  
  
numbers = [3, 7, 12, 18, 21]
       info = {"city": "Tunis", "job": "Student"}
       data_tuple = ("Python", "Data Engineering", "Projects")



 print(greet(name))
 print(f"ID of age variable: {id(age)}")
    




    if age < 18:
        print("Minor")
    elif 18 <= age < 30:
        print("Young Adult")
    else:
        print("Adult")


 print("\nFor loop mit  enumerate:")
  for idx, num in enumerate(numbers):
 print(f"Index {idx}: {num}")


##loop normal , step + 
print("\nWhile loop:")
 counter = 0

 while counter < len(numbers):
 print(f"Counter {counter}: {numbers[counter]}")
 counter += 1



#il va trouve la case memoire de nbr 15
    str_num = "15"
    int_num = int(str_num)
    print(f"\nString '{str_num}' casted to integer: {int_num}")

    result = add_numbers(8, 12)
    print(f"\n8 + 12 = {result}")


       if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Python Fundamentals Data Analyzer")
        parser.add_argument("--name", type=str, help="Enter your name", default="Ons")
        parser.add_argument("--age", type=int, help="Enter your age", default=23)
        args = parser.parse_args()

    print(f"Command line input - Name: {args.name}, Age: {args.age}\n")
    
    main()
