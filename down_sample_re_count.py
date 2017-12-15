from __future__ import print_function
import synapseclient
import os
import sys


def pull_data(synId, syn):
    # 1. pull file into local directory
    # 2. syn = synapseclient.Synapse()
    entity = syn.get(synId, downloadLocation='./')
    print("file downloaded")
    return entity.path, entity.annotations


def run_samtools(fileName):
    print("running samtools")
    str = ''.join(['samtools view -b -s 0.5 ', fileName,
                   ' > ', fileName, '_new.bam'])
    os.system(str)
    print("samtools run")
    str2 = ''.join([fileName, '_new.bam'])
    return str2


def run_htseq(fileName, gtfFileName):
    str = ''.join(['htseq-count -f bam ', fileName, ' ', gtfFileName,
                   ' > ', fileName, '_counts.txt'])
    print("running htseq")
    os.system(str)
    print("htseq run")
    str2 = ''.join([fileName, '_counts.txt'])
    return str2


def push_to_synapse(fileName, uploadLocation, synId, annotations, syn):
    annotations['fileFormat'] = ['txt']
    entity = synapseclient.File(
            fileName,
            parentId=uploadLocation,
            used=synId,
            executed='https://github.com/Sage-Bionetworks'
                     '/DockerRNAseq/blob/master/Dockerfile')
    entity = syn.store(entity)
    print("uploaded to synapse")


if __name__ == '__main__':
    synId = sys.argv[1]
    uploadLocation = sys.argv[2]
    print("input", synId)
    print("output location", uploadLocation)
    syn = synapseclient.login(
            os.environ['synapseUser'],
            os.environ['synapsePassword'])
    print("logged in")
    local_path, annotations = pull_data(synId, syn)
    sam_output = run_samtools(local_path)
    htseq_output = run_htseq(
            sam_output,
            "/app/gencode.v24.primary_assembly.annotation.gtf")
    push_to_synapse(htseq_output, uploadLocation, synId, annotations, syn)
