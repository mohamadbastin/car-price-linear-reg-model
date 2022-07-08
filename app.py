import pickle
from random import randint
import pandas as pd
from sklearn.linear_model import LinearRegression
from tkinter import *
from tkinter.constants import *
# from awesometkinter.bidirender import add_bidi_support, render_text

def clear():
    for field in fields:
        field.delete(0, END)

def input_random_test():
    clear()
    test_data = pd.read_csv('cars-test.csv').dropna().drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
    sample_car = test_data.loc[randint(0, len(test_data.index) - 1), :].values.tolist()
    # Testing
    for i in range(len(fields)):
        fields[i].insert(0, sample_car[i])

def insert():
    if any(field.get() == "" for field in fields):
        print("empty input")
    else:
        # Helper function to parse input data into appropriate types
        def parse_element(str):
            if str.isdigit():
                return int(str)
            else:
                try:
                    return float(str)
                except ValueError:
                    return str
        # Transform the input for the model
        car_details = [parse_element(field.get()) for field in fields]
        car_df_raw = pd.DataFrame([car_details], columns = field_labels)
        car_df = pd.get_dummies(car_df_raw)
        car_df = car_df.reindex(labels=model_meta, axis=1, fill_value=0)
        # Predict the price
        predicted_price = model.predict(car_df)
        # Show the price
        output_str = f"The predicted price is: {format(predicted_price[0].astype('int64'), ',')}"
        output_text.config(text=output_str)

if __name__ == "__main__":

    # Load Column Names, Model
    try:
        field_labels = pickle.load(open('input_columns.sav', 'rb'))
        model_meta = pickle.load(open('model_meta.sav', 'rb'))
        model = pickle.load(open('model.sav', 'rb'))
    except:
        print("Can't load model metadata.")

    root = Tk()
 
    root.configure(background='light blue')
 
    root.title("Car Price Prediciton")
 
    root.geometry("680x700")

    form_frame = Frame()
    form_frame.configure(background='light blue')

    heading = Label(form_frame, text="Car Details Form", bg="light blue", font='any 20')
    heading.grid(row=0, column=1)

    fields = []
    for i in range(len(field_labels)):
        new_label = Label(form_frame, text=field_labels[i], bg="light blue", font='any 15', relief=RAISED)
        new_label.grid(row=i+1, column=0, pady=5, padx=6, sticky='ew')
        new_label_field = Entry(form_frame, font='any 17')
        new_label_field.grid(row=i+1, column=1, ipadx="100", pady=5, padx=10)
        # add_bidi_support(new_label_field)
        fields.append(new_label_field)

    submit = Button(form_frame, text="Submit", fg="Black", font='any 15',
                            bg="Red", command=insert)
    submit.grid(row=len(field_labels) + 1, column=1, pady=10)

    randomize = Button(form_frame, text="Randomize", fg="Black", font='any 15', bg='white', command=input_random_test)
    randomize.grid(row=len(field_labels) + 1, column=0)

    form_frame.grid(row=0, sticky='ew')

    output_frame = Frame()
    output_frame.configure(background='light blue')
    output_text = Label(output_frame, text="", bg='light blue', font='any 16')
    output_text.grid(row=0, column=0)
    output_frame.grid(row=1, sticky='ew', padx=10, pady=10)
 
    root.mainloop()