# BRaIn

## Improved IR-based Bug Localization with Intelligent Relevance Feedback [📎](https://arxiv.org/abs/2501.10542)
Accepted Paper at ICPC 2025 \
[Pre-print](https://arxiv.org/abs/2501.10542)
> Asif Mohammed Samir and Mohammad Masudur Rahman. _The 33rd IEEE/ACM International
Conference on Program Comprehension (ICPC 2025), Ottawa, Canada._

##
## Abstract
Software bugs pose a significant challenge during development and maintenance, and practitioners spend nearly 50% of their time dealing with bugs. Many existing techniques adopt Information Retrieval (IR) to localize a reported bug using textual and semantic relevance between bug reports and source code. However, they often struggle to bridge a critical gap between bug reports and code that requires in-depth contextual understanding, which goes beyond textual or semantic relevance. In this paper, we present a novel technique for bug localization - BRaIn - that addresses the contextual gaps by assessing the relevance between bug reports and code with Large Language Models (LLM). It then leverages the LLM's feedback (a.k.a., Intelligent Relevance Feedback) to reformulate queries and re-rank source documents, improving bug localization. We evaluate BRaIn using a benchmark dataset, Bench4BL, and three performance metrics and compare it against six baseline techniques from the literature. Our experimental results show that BRaIn outperforms baselines by 87.6%, 89.5%, and 48.8% margins in MAP, MRR, and HIT@K, respectively. Additionally, it can localize approximately 52% of bugs that cannot be localized by the baseline techniques due to the poor quality of corresponding bug reports. By addressing the contextual gaps and introducing Intelligent Relevance Feedback, BRaIn advances not only theory but also improves IR-based bug localization.

## Project Structure
   The project structure is as follows:
   * `Data`: Contains the dataset in json format. 
   * `Output`: Contains the output of each stage of the BRaIn.
   * `src`: Contains the source code for the project.
     - BRaIn: Contains the source code for replicating the BRaIn tool.
     - IR: Contains the source code for the IR tool (e.g., indexing).
     - java: Contains the source code for the Java files for collecting source code segments.
   * `requirements.txt`: Contains the required python packages for the project.
   * `README.md`: Contains the project documentation.

## Dataset
   The refined Bench4BL dataset used for this project is provided in the `data` directory in json format. The dataset contains the following fields:
   - `bug_id`: Unique identifier for the bug.
   - `bug_title`: Title of the bug.
   - `bug_description`: Description of the bug.
   - `project`: Project to which the bug belongs.
   - `sub_project`: Subject to which the bug belongs.
   - `version`: Version of the project.
   - `fixed_version`: Version in which the bug was fixed.
   - `fixed_files`: Files in which the bug was fixed as a json array.


## Pre-requisites
   The following are the pre-requisites for the project:
   * Python 3.10
   * Elasticsearch
   * NVIDIA CUDA enabled GPU
   * Required Python Packages
   * Instruct models from Hugging Face with 8 bit Quantization (e.g., [Mistral](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GPTQ))

## Installing Required Packages

### Python 3.10:
> We recommend using a virtual environment to install the packages and run the application.
> Learn to use a virtual environment [here](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/).

#### Windows:

1. **Download Python 3.10:**  
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download the Windows installer (`Windows Installer (64-bit)` recommended).
   - Run the installer.
   - Check the box to add Python to PATH during installation.

2. **Verify Installation:**  
   - Open Command Prompt.
   - Type `python --version`.
   - You should see `Python 3.10.x`.

#### Linux (Ubuntu/Debian):

1. **Install Python 3.10:**  
   - Open Terminal.
   - Run the following commands:
     ```
     sudo apt update
     sudo apt install python3.10
     ```

2. **Verify Installation:**  
   - Type `python3.10 --version`.
   - You should see `Python 3.10.x`.


### Install PyTorch:
PyTorch with CUDA support is required for the project. The following example installs PyTorch with CUDA 11.3 support which used in our experiments.

Use the following command to install PyTorch with CUDA support:
> ```
> pip install torch==1.10.0+cu113 torchvision==0.11.0+cu113 torchaudio==0.10.0+cu113 torchtext==0.11.0 -f https://download.pytorch.org/whl/cu113/torch_stable.html
> ```
Verify the installation by running the following command:
> ```
> python -c "import torch; print(torch.cuda.is_available())"
> ```
You should see `True` if PyTorch is installed correctly with CUDA support.

If you do not have a CUDA-enabled GPU, install the CPU version of PyTorch.
Learn more about PyTorch with CUDA support and working with other versions [here](https://pytorch.org/get-started/locally/).

### Elasticsearch:

#### Windows:

1. **Download Elasticsearch:**
   - Visit [elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch).
   - Download the ZIP package for Windows.

2. **Extract and Start Elasticsearch:**  
   - Extract the downloaded ZIP file.
   - Navigate to the extracted directory.
   - Run `bin\elasticsearch.bat` in Command Prompt.

3. **Verify Installation:**  
   - Open a web browser.
   - Go to [http://localhost:9200](http://localhost:9200).
   - Check for a JSON response indicating Elasticsearch is running.

#### Linux (Ubuntu/Debian):

1. **Download and Install Elasticsearch:**  
   - Open Terminal.
   - Run the following commands:
     ```
     wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<version>-amd64.deb
     sudo dpkg -i elasticsearch-<version>-amd64.deb
     ```

2. **Start Elasticsearch Service:**  
   - Run:
     ```
     sudo systemctl start elasticsearch
     sudo systemctl enable elasticsearch
     ```

3. **Verify Installation:**  
   - Open a web browser.
   - Go to [http://localhost:9200](http://localhost:9200).
   - Ensure Elasticsearch is running by checking for a JSON response.


### Install Required Python Packages:

1. **Navigate to Project Directory:**
   - Open terminal/command prompt.
   - Use `cd` to move to the directory containing `requirements.txt`.

2. **Install Packages:**
   - Run `pip install -r requirements.txt`.

## Replicate

1. Index Documents in Elasticsearch for Each version of the Project::
   - Run 'src/IR/Indexer/Index_Creator.py' to create an index in Elasticsearch. The configuration for the index is provided in 'IR_Config.yaml'.
   - Extract the source files from Git Projects per version and index them in Elasticsearch using 'Indexer.py'. The GitHub Repositories are listed in the [Bench4BL](https://github.com/exatoa/Bench4BL) repository.
   - The default port for Elasticsearch is 9200.
2. Running **BRaIn**: 
 
   a. **Cache Intially Retrieved Documents**: 
      - Run `src/BRain/a_Cache_initial_search_files.py` to cache the documents from Elasticsearch. This script retrieves the documents from Elasticsearch and collect code segments from the source files using py4j using [Java Parser](https://javaparser.org/). 'java' package contains the Java files for collecting source code segments in compressed format.
   
   b. **Generate Intelligent Relevance Feedback (IRF)**:
      - Run `src/BRain/b_GenerateFeedback.py` to generate Intelligent Relevance feedback (IRF) for the bugs in step-2a. This stage, BRaIn requires CUDA enabled GPU and GPTQ quantized models from Huggingface. Define the model and other parameters in the source file before running the code. This source code is specifically configured for GPTQ models with 8 bit quantization.
   
   c. **Ranking and Scoring**:
      - Run `src/BRain/c_PRF_Scoring_cache.py` to re-rank using query collected using CodeRank from based on Intelligent Relevance Feedback (IRF) and then re-score the documents based on the IRF collected in step-2b. (To streamline the re-ranking process during research using Elasticsearch, we created second index in Elasticsearch, with bug_id as the document id to retrieve documents to re-rank based on the bug_id. If you plan to use re-rank using Elasticsearch, please index the top-N documents retrieved from Elasticsearch using a additional field 'bug_id' along with other fields in step-a. The configuration for the index is provided in 'IR_Config.yaml' in 'IR_Reretrieval/config'.)
 
   d. **Evaluate Performance**:
      - Run `src/BRain/d_Rank_Performance.py` to evaluate the performance of the BRaIn in step-2c. It will return the MAP, MRR, and HIT@K scores for the BRaIn. You can define K (e.g., 1, 5, 10) of HIT@K in the source file.



## Citation

If you find this work useful for your research, please consider citing it.

### ICPC 2025 (Conference Version)
[Improved IR-based Bug Localization with Intelligent Relevance Feedback](https://conf.researchr.org/details/icpc-2025/icpc-2025-research/32/Improved-IR-based-Bug-Localization-with-Intelligent-Relevance-Feedback)

```bibtex
@inproceedings{samir2025improvedirbasedbuglocalization,
  title     = {Improved IR-based Bug Localization with Intelligent Relevance Feedback},
  author    = {Asif Mohammed Samir and Mohammad Masudur Rahman},
  booktitle = {Proceedings of the 33rd IEEE/ACM International Conference on Program Comprehension (ICPC)},
  year      = {2025},
  note      = {To appear}
}


[//]: # (   )
@misc{samir2025improvedirbasedbuglocalization,
  title        = {Improved IR-based Bug Localization with Intelligent Relevance Feedback},
  author       = {Asif Mohammed Samir and Mohammad Masudur Rahman},
  year         = {2025},
  eprint       = {2501.10542},
  archivePrefix= {arXiv},
  primaryClass = {cs.SE},
  url          = {https://arxiv.org/abs/2501.10542}
}


