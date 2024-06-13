import re

research_areas = [
    "Processor, memory, and storage systems architecture",
    "Parallelism: instruction, thread, data, multiprocessor",
    "Datacenter-scale computing",
    "IoT, mobile, and embedded architecture",
    "Interconnection network, router, and network interface architectures",
    "Architectures for emerging applications including machine learning and bioinformatics",
    "Architectural support for programming languages or software development",
    "Architectural support for interfacing with accelerators",
    "Architectural support for security, virtual memory, and virtualization",
    "Dependable processor and system architecture",
    "Architectures for emerging technologies including novel circuits, memory technologies, quantum computing, etc.",
    "Architecture modeling, simulation methodologies, and tools",
    "Evaluation and measurement of real computing systems",
    "No area of preference"
]

workshops_tutorials = {
    'Workshop: Emerging Vision and Graphics Systems and Architectures' : 0,
    'Tutorial: Memory-Centric Computing Systems' : 0,
    'Workshop: AI for Full-Automated Chip Design: Gimmick or Trend?' : 0,
    'Workshop: DRAM Security' : 0,
    'Tutorial: GENESYS: Open-Source Parameterizable NPU Generator with Full-Stack Multi-Target Compilation Stack' : 0,
    'Workshop: 8th Workshop on Cognitive Architectures' : 0,
    'Tutorial: Agile Software-Hardware Co-Design of AI-Centric Heterogeneous SoCs' : 0,
    'Tutorial: gem5' : 0,
    'Tutorial: I too can Quantum (I2Q): Classical Infrastructure for Fault-Tolerant Quantum Computers' : 0,
    'Workshop: Third Workshop on Open-Source Computer Architecture Research' : 0,
    'Workshop: Acceleration and Optimization of Multi-modal Computing' : 0,
    'Tutorial: Designing for the Neural Processing Unit on AMD’s Ryzen AI with Open-Source Tools' : 0,
    'Tutorial: Expedited development of novel RISC-V instructions through an emulation-simulation framework' : 0,
    'Tutorial: The ESP Approach to Agile Chip Design' : 0,
    'Workshop: Domain Specific System Architecture' : 0,
    'Tutorial: REMU: System-level Evaluation and Debugging with a Custom FPGA-based Emulation Framework' : 0,
    'Tutorial: Simulation for Processing Using Memory Systems' : 0,
    'Tutorial: SODA Synthesizer: Accelerating Artificial Intelligence Applications with an End-to-End Silicon Compiler' : 0,
    'Workshop: New Approaches for Addressing the Computing Requirements of LLMs and GNNs' : 0,
    'Workshop: Practical Symbiosis of Machine Learning, Computer Architecture, and Systems' : 0,
    'Tutorial and Workshop: Systems and Architectures for Visual Computing' : 0,
    'Workshop: Undergraduate Architecture Mentoring' : 0,
    'Tutorial: Simulation Framework for Design Exploration of Heterogeneous and Multi-Chip Manycore Systems' : 0
}

student_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Dissability', 'Visa', 'Postal', 'Workshops', 'MaSA Mentee', 'ResearchAreasMaSA', 'ResearchAreas2MaSA', 'ResearchAreas3MaSA', 'MaSS Mentee', 'ResearchAreasMaSS', 'MaSS Mentor', 'ResearchAreasMentors', 'ResearchAreasGeneral', 'Eulogy', 'Retiring', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']

studentMember_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Dissability', 'Visa', 'Postal', 'ACM/IEEE Number', 'Workshops', 'MaSA Mentee', 'ResearchAreasMaSA', 'ResearchAreas2MaSA', 'ResearchAreas3MaSA', 'MaSS Mentee', 'ResearchAreasMaSS', 'MaSS Mentor', 'ResearchAreasMentors', 'ResearchAreasGeneral', 'Eulogy', 'Retiring', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']

studentUarch_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Dissability', 'Visa', 'Postal', 'Workshops', 'MaSA Mentee', 'ResearchAreasMaSA', 'ResearchAreas2MaSA', 'ResearchAreas3MaSA', 'MaSS Mentee', 'ResearchAreasMaSS', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']

senior_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Dissability', 'Visa', 'Postal', 'Workshops', 'MaSA Mentor', 'IndustryOrAcademia', 'IndustryOrAcademia2', 'ResearchAreas', 'ResearchAreasMentors/Mentees','Eulogy', 'Retiring', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']

seniorMember_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Dissability', 'Visa', 'Postal', 'ACM/IEEE Number', 'Workshops', 'MaSA Mentor', 'IndustryOrAcademia', 'IndustryOrAcademia2', 'ResearchAreas', 'ResearchAreasMentors/Mentees','Eulogy', 'Retiring', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']

seniorOthers_categories = ['Date', 'First Name', 'Last Name', 'Email', 'Work Phone', 'Job Title', 'Affiliation', 'Location', 'Workshop - Saturday', 'Workshop - Sunday', 'Workshop - Two days', 'Dissability', 'Visa', 'Postal', 'MaSA Mentor', 'IndustryOrAcademia', 'MaSS/MaSA Mentee', 'MaSS Mentee', 'MaSS Mentor', 'ResearchAreas', 'Eulogy', 'Retiring', 'Policy', 'First Name (Buyer)', 'Last Name(Buyer)', 'Email(Buyer)', 'Ticket Type']


def parse_text(text):
    # Define the regex pattern to match "Workshop:", "Tutorial:", and "Tutorial and Workshop:"
    pattern = r'(Workshop:.*?)(?=Workshop:|Tutorial:|Tutorial and Workshop:|$)|(Tutorial:.*?)(?=Workshop:|Tutorial:|Tutorial and Workshop:|$)|(Tutorial and Workshop:.*?)(?=Workshop:|Tutorial:|Tutorial and Workshop:|$)'
    
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    
    # Extract the non-empty groups
    result = [match[0] or match[1] or match[2] for match in matches]
    result = [item.strip().rstrip(',') for item in result]

    
    return result
