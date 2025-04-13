import json

# default preferences
toneChoice=1
lengthChoice=1
numArticles=5

tones={0: 'a friendly, casual tone', 1: 'a formal, business-style tone'}
lengths={0: '1 short 3-5 sentence paragraph', 1: '3 brief paragaphs'}
print(tones[toneChoice])
print("Welcome to Personal Press!")
print("Set your news preferences to begin getting a daily news digest.")
print("""Select the number of the tone your would like to recieve email summaries in:
      (0) a friendly, casual tone
      (1) a formal, business-style tone
      """)

while (True):
    toneChoice = int(input("Enter a valid number: "))
    if toneChoice==0 or toneChoice==1:
        break
    
print("""Select the length of the email summaries you recieve:
    (0) 1 short 3-5 sentence paragraph
    (1) 3 brief paragaphs
    """)
while (True):
    lengthChoice = int(input("Enter a valid number: "))
    if lengthChoice==0 or lengthChoice==1:
        break
    
print("What email would you like to recieve your news digest?")
email = input("Enter a valid email: ")

print("How many article summaries would you like to recieve in your news digest(1-15)?")
while (True):
    numArticles = int(input("Enter a valid number: "))
    if numArticles>0 or numArticles<=15:
        break

print("Preferences are set! Expect your news digest everday at 8am")
# Data to save
preferences = {"tone": tones[toneChoice], "length": lengths[lengthChoice], "email": email, "numArticles":  numArticles}                                          
# Save the data to a file
with open("userPreferences.json", "w") as f:
    json.dump(preferences, f)