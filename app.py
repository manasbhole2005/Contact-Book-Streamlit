import streamlit as st
import json
import os
import pandas as pd

FILE = "contacts.json"

st.set_page_config(page_title="Contact Book", layout="wide")

def load_contacts():
    if not os.path.exists(FILE):
        with open(FILE,"w") as f:
            json.dump([],f)
    with open(FILE,"r") as f:
        return json.load(f)

def save_contacts(data):
    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)

contacts = load_contacts()

st.sidebar.title(" Contact Book")
menu = st.sidebar.radio(
    "Menu",
    ["Add Contact","View Contacts","Search Contact","Update Contact","Delete Contact"]
)

st.title("Contact Book")

if menu=="Add Contact":
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    address = st.text_area("Address")

    if st.button("Add Contact"):
        if name=="" or phone=="":
            st.warning("Name and Phone are required.")
        elif any(c["phone"]==phone for c in contacts):
            st.error("Phone number already exists.")
        else:
            contacts.append({
                "name":name,
                "phone":phone,
                "email":email,
                "address":address
            })
            save_contacts(contacts)
            st.success("Contact Added Successfully!")

elif menu=="View Contacts":
    st.subheader("All Contacts")

    if contacts:
        df = pd.DataFrame(contacts)
        st.dataframe(df,use_container_width=True)
        st.metric("Total Contacts",len(contacts))
    else:
        st.info("No contacts found.")

elif menu=="Search Contact":
    keyword = st.text_input("Enter Name or Phone")

    if keyword:
        result=[]
        for c in contacts:
            if keyword.lower() in c["name"].lower() or keyword in c["phone"]:
                result.append(c)

        if result:
            st.dataframe(pd.DataFrame(result),use_container_width=True)
        else:
            st.warning("No Contact Found.")

elif menu=="Update Contact":
    if contacts:
        names=[c["name"] for c in contacts]
        selected=st.selectbox("Select Contact",names)
        index=names.index(selected)

        new_name=st.text_input("Name",contacts[index]["name"])
        new_phone=st.text_input("Phone",contacts[index]["phone"])
        new_email=st.text_input("Email",contacts[index]["email"])
        new_address=st.text_area("Address",contacts[index]["address"])

        if st.button("Update"):
            duplicate=False
            for i,c in enumerate(contacts):
                if i!=index and c["phone"]==new_phone:
                    duplicate=True
            if duplicate:
                st.error("Phone already exists.")
            else:
                contacts[index]={
                    "name":new_name,
                    "phone":new_phone,
                    "email":new_email,
                    "address":new_address
                }
                save_contacts(contacts)
                st.success("Contact Updated!")
    else:
        st.info("No contacts available.")

elif menu=="Delete Contact":
    if contacts:
        names=[c["name"] for c in contacts]
        selected=st.selectbox("Select Contact",names)

        if st.button("Delete Contact"):
            contacts=[c for c in contacts if c["name"]!=selected]
            save_contacts(contacts)
            st.success("Contact Deleted!")
    else:
        st.info("No contacts available.")

st.divider()
st.caption("Developed using Python & Streamlit")
