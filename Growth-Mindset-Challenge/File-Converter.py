import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", page_icon="📂")
st.title("File Converter")
st.write("Upload a file and convert it to another format.")

file = st.file_uploader("Upload a file", type=["csv", "xlsx", "json", "parquet"])

if file:
    ext = file.name.split(".")[-1]

    # Read the file based on its extension
    if ext == "csv":
        df = pd.read_csv(file)
    elif ext == "xlsx":
        df = pd.read_excel(file, engine="openpyxl")
    elif ext == "json":
        df = pd.read_json(file)
    elif ext == "parquet":
        df = pd.read_parquet(file)
    else:
        st.error("Unsupported file format!")
        st.stop()

    st.subheader(f"{file.name} - Preview")
    st.dataframe(df.head())

    if st.checkbox(f"Remove Duplicates - {file.name}"):
        df.drop_duplicates(inplace=True)
        st.write("Duplicates removed!")
        st.dataframe(df.head())

    if st.checkbox(f"Fill Missing Values - {file.name}"):
        df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
        st.success("Missing values filled!")
        st.dataframe(df.head())

    selected_columns = st.multiselect(f"Select columns to keep - {file.name}", df.columns, default=df.columns)
    df = df[selected_columns]
    st.dataframe(df.head())

    if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

    format = st.radio(f"Convert {file.name} to", ["csv", "xlsx", "json", "parquet"])

    if st.button(f"Download {file.name} as {format}"):
        output = BytesIO()
        mime = ""
        new_filename = file.name.rsplit(".", 1)[0] + f".{format}"

        if format == "csv":
            df.to_csv(output, index=False)
            mime = "text/csv"
        elif format == "xlsx":
            df.to_excel(output, index=False, engine="openpyxl")
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format == "json":
            df.to_json(output, orient="records")
            mime = "application/json"
        elif format == "parquet":
            df.to_parquet(output, index=False)
            mime = "application/octet-stream"

        output.seek(0)
        st.download_button(label=f"Download {new_filename}", data=output, file_name=new_filename, mime=mime)

        st.success("Process completed!")
