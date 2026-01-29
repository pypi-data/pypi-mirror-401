#!/usr/bin/env python

from Bio import SeqIO
import re
import pandas as pd
import argparse
import os

#    - Genome name, species, SCCmec extraction success/failure
#    - Extracted SCCmec length
#    - Number of att sites found
#    - Any error messages 

class Species():
    """This class will extract the species information from the input genome"""
    
    def __init__(self, genome_file: str, metadata_file: str):
        
        self.genome = genome_file
        self.metadata = pd.read_csv(metadata_file, sep = "\t")
        
    def extract_accession(self):
        """Extract the accession number from input genome"""
        
        # Example file name GCF_000011925.1_ASM1192v1_genomic.fna
        
        accession_pattern = r"(GCF_\d+\.\d+)" 

        return re.findall(accession_pattern, self.genome)

    def obtain_species(self):
        """Take obtained accession and find corresponding species from metadata file"""

        accession = self.extract_accession()

        # Use query to check for accession in "Accession" and reutrn value in corresponding row of "Organism"
        # We use '@' to let pandas know it is to use a python variable rather than a string
        species = self.metadata.query("Accession == @accession")["Organism"]

        return species.values[0]
    
class SCCmecExtractionStats():
    """This class will extract SCCmec associated stats"""

    def __init__(self, genome_name: str, sccmec_dir: str):

        self.genome_name = genome_name
        self.sccmec_dir = sccmec_dir

    def sccmec_extraction(self):
        """Checks if SCCmec Extraction was successful"""

        accession_pattern = r"(GCF_\d+)"
        out_name = re.findall(accession_pattern, self.genome_name)
        sccmec_out_name = out_name[0] + "_SCCmec.fasta"
        self.sccmec_extracted = False

        self.extracted_sccmec_fasta = os.path.join(self.sccmec_dir, sccmec_out_name)

        if not os.path.exists(self.extracted_sccmec_fasta):
            # This means no SCCmec was extracted, so self.sccmec_extracted remains False
            return "FAILED", self.sccmec_extracted, 0
        
        try:
            self.sccmec_extracted = True
            record = SeqIO.read(self.extracted_sccmec_fasta, "fasta")
            return "SUCCESS", self.sccmec_extracted, len(record.seq)
        
        except Exception as e:
            return f"FAILED: {str(e)}", self.sccmec_extracted, 0

class AttSiteStats():
    """Class for obtaining att site stats"""

    def __init__(self, fasta, att_site_file: str):

        self.att_site_file = pd.read_csv(att_site_file, sep = "\t")
        self.genome_name = re.findall(r"(GCF_\d+)", fasta)

    def count_att_sites(self):
        """Count number of att sites obtained for a given genome"""

        att_sites = self.att_site_file.query("Input_File == @self.genome_name")["Pattern"]

        # If we want to just count the number of att sites identified without being concerned about type
        return len(att_sites)

class StatsLogger():
    """Main class that brings together all the outputs"""

    def __init__(self, species, sccmec_stats, total_att_sites):

        self.species = species
        self.sccmec_stats = sccmec_stats
        self.total_att_sites = total_att_sites
        
    def generate_stats(self, outfile: str):
        """Generate our stats and save to file."""

        try:
            # Extract the stats
            species_name = self.species.obtain_species()
            sccmec_success, sccmec_file, sccmec_length = self.sccmec_stats.sccmec_extraction()
            total_att_sites_count = self.total_att_sites.count_att_sites()

            # Create results
            # Square brackets change the values from scalar, meaning you do not need to pass an index when creating a DataFrame
            results = {
                        "genome_id": [self.species.genome],
                        "species": [species_name],
                        "sccmec_extracted": [sccmec_success],
                        "sccmec_size": [sccmec_length],
                        "num_att_sites": [total_att_sites_count]
            }
        
            results_df = pd.DataFrame(results)
            results_df.to_csv(outfile, sep = "\t", index = False, mode = 'a', header = not os.path.exists(outfile))
            return results_df
        
        except Exception as e:
            print(f"Error generating stats: {e}")
            return None


def main():
    """Define main parser"""

    parser = argparse.ArgumentParser(description = "Process input FASTA and extract species from Metadata file.")
    parser.add_argument("-f", "--fasta", required = True, help = ".fasta to obtain species for.")
    parser.add_argument("-m", "--metadata", required = True, help = "Metadata data file in .tsv format")
    parser.add_argument("-a", "--att_sites", required = True, help = "TSV file containing att site information.")
    parser.add_argument("-s", "--sccmec_dir", required = True, help = "Directory containing extracted SCCmec sequences.")
    parser.add_argument("-o", "--outfile", required = True, help = "Provide name of outfile to store stats.")
    args = parser.parse_args()

    try:
        # Create class objects with required inputs
        species_extraction = Species(args.fasta, args.metadata)
        sccmec_stats = SCCmecExtractionStats(args.fasta, args.sccmec_dir)
        att_site_stats = AttSiteStats(args.fasta, args.att_sites)

        # Create stats logger and pass class objects
        stats_logger = StatsLogger(species_extraction, sccmec_stats, att_site_stats)
        results = stats_logger.generate_stats(args.outfile)

        if results is not None:
            print(f"Stats have been generated: {args.outfile}")
        else:
            print("There has been an error and stats have not been generated.")

    except Exception as e:
        print(f"Error in main execution: {e}")
    

if __name__ == "__main__":
    main()