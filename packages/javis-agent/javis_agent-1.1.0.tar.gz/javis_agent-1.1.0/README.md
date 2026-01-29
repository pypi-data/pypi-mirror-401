# Javis Agent
## Create virual environment
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
// Check latest version
apt list | grep python3.14
sudo apt install python3.14 python3.14-venv python3.14-dev
python3.14 -m venv venv
source venv/bin/activate
python --version (show 3.14 version)
pip install langchain langchain_openai dotenv pypdf pdfplumber python-docx openpyxl pandas python-pptx



