import sys
import pickle
import pandas as pd
import numpy as np
import pycaret.regression as pycreg
from random import randint
from tkinter.ttk import Combobox
from sklearn.linear_model import LinearRegression
from tkinter import *
from tkinter.constants import *

def clear():
    for field in fields:
        if field.winfo_class() == 'TCombobox':
            field.config(state='normal')
            field.delete(0, END)
            field.config(state='readonly')
        else:
            field.delete(0, END)

def input_random_test():
    clear()
    test_data = pd.read_csv('cars-test3.csv').dropna().reset_index(drop=True).drop('price', axis=1).drop('_id', axis=1).drop('url', axis=1)
    sample_car = test_data.loc[randint(1, len(test_data.index) - 1), :].values.tolist()
    for i in range(len(fields)):
        if fields[i].winfo_class() == 'TCombobox':
            fields[i].config(state='normal')
            fields[i].insert(0, sample_car[i])
            fields[i].config(state='readonly')
        else:
            fields[i].insert(0, sample_car[i])

def insert():
    if any(field.get() == "" for field in fields):
        output_str = "Please fill all of the fields."
        output_text.config(text=output_str)
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
        car_df_raw = pd.DataFrame([car_details], columns = [field['name'] for field in input_fields])

        if model_type == 'rf':
            predicted_price = pycreg.predict_model(model, car_df_raw)
            prediction = predicted_price['Label'][0].astype('int64')

        else:
            car_df = pd.get_dummies(car_df_raw)
            car_df = car_df.reindex(labels=model_meta, axis=1, fill_value=0)
            predicted_price = model.predict(car_df)
            prediction = predicted_price[0].astype('int64')

        output_str = f"The predicted price is: {format(prediction, ',')}"
        output_text.config(text=output_str)
        if (estimated_price_field.get() != ""):
            eprice = int(estimated_price_field.get())
            if (abs(eprice - prediction) < 40000000):
                verdict_str = f"Your estimation is close enough!"
            elif (eprice > prediction):
                verdict_str = f"Your estimation is higher than our prediction."
            elif (eprice < predicted_price):
                verdict_str = f"Your estimation is lower than our prediction."
            verdict_text.config(text=verdict_str)
        else:
            verdict_text.config(text='')


if __name__ == "__main__":

    # Choose model type (lr=linear regression, rf=random forest)
    model_type = sys.argv[1] if len(sys.argv) > 1 else None

    # Load Column Names, Model
    try:
        input_fields = pickle.load(open('input_columns.sav', 'rb'))
        if model_type == 'rf':
            model = pycreg.load_model("rf")
        else:
            model_meta = pickle.load(open('model_meta.sav', 'rb'))
            model = pickle.load(open('model.sav', 'rb'))
    except:
        print("Can't load model metadata.")
    

    root = Tk()
 
    root.configure(background='light blue')
 
    root.title("Car Price Prediciton")
 
    root.geometry("680x780")

    form_frame = Frame()
    form_frame.columnconfigure(1, weight=1)
    form_frame.configure(background='light blue')

    heading = Label(form_frame, text="Car Details Form", bg="light blue", font='any 20')
    heading.grid(row=0, column=1)

    fields = []
    for i, field in enumerate(input_fields):
        new_label = Label(form_frame, text=field['name'], bg="light blue", font='any 15', relief=RAISED)
        new_label.grid(row=i+1, column=0, pady=5, padx=6, sticky='ew')
        if field['type'] == object:
            new_label_field = Combobox(form_frame, state='readonly', font='any 17')
            new_label_field['values'] = field['unique_vals'].tolist()
            new_label_field.grid(row=i+1, column=1, ipadx="91", pady=5, padx=10)
        else:
            new_label_field = Entry(form_frame, font='any 17')
            new_label_field.grid(row=i+1, column=1, ipadx="100", pady=5, padx=10)
        fields.append(new_label_field)

    estimated_price = Label(form_frame, text="Estimated Price", bg="light blue", font="any 15", relief=RAISED)
    estimated_price.grid(row=len(input_fields) + 1, column=0, pady=5, padx=6, sticky='ew')
    estimated_price_field = Entry(form_frame, font='any 17')
    estimated_price_field.grid(row=len(input_fields) + 1, column=1, ipadx="100", pady=5, padx=10)

    submit = Button(form_frame, text="Predict", fg="Black", font='any 15',
                            bg="Red", command=insert)
    submit.grid(row=len(input_fields) + 2, column=1, pady=10)

    randomize = Button(form_frame, text="Randomize", fg="Black", font='any 15', bg='white', command=input_random_test)
    randomize.grid(row=len(input_fields) + 2, column=0)

    form_frame.grid(row=0, sticky='ew')

    output_frame = Frame()
    output_frame.configure(background='light blue')
    output_text = Label(output_frame, text="", bg='light blue', font='any 20')
    output_text.grid(row=0, column=0, sticky='w')
    verdict_text = Label(output_frame, text="", bg='light blue', font='any 18')
    verdict_text.grid(row=1, column=0, sticky='w')
    output_frame.grid(row=1, padx=25, pady=10, sticky='ew')
    
 
    root.mainloop()