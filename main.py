import os
import sys

def main():
    print("Starting Cryptocurrency Time Series Analysis Dashboard...")
    os.chdir("Member3_GUI_Visualization")
    os.system("python -m streamlit run app.py")

if __name__ == "__main__":
    main()
