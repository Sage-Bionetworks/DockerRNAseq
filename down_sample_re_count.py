import synapseclient, os, sys

def pull_data(synId):
    #1. pull file into local directory
    #2. syn = synapseclient.Synapse()
    syn = synapseclient.Synapse()
    syn.login(os.environ['synapseUser'],os.environ['synapsePassword'])
    print("logged in")
    entity = syn.get(synId,downloadLocation = './')
    print("file downloaded")
    bar = entity.path
    return(bar)
    #get file name from the entity object
    #return...

def run_samtools(fileName):
    print("running samtools")
    str = ''.join(['samtools view -b -s 0.5 ',fileName,' > ',fileName,'_new.bam'])
    os.system(str)
    print("samtools run")
    str2 = ''.join([fileName,'_new.bam'])
    return(str2)

def run_htseq(fileName,gtfFileName):
    str = ''.join(['htseq-count -f bam ',fileName,' ',gtfFileName,' > ',fileName,'_counts.txt'])
    print("running htseq")
    os.system(str)
    print("htseq run")
    str2 = ''.join([fileName,'_counts.txt'])
    return(str2)

def push_to_synapse(fileName,uploadLocation):
    syn = synapseclient.Synapse()
    syn.login(os.environ['synapseUser'],os.environ['synapsePassword'])
    entity = synapseclient.File(fileName,parentId = uploadLocation)
    entity = syn.store(entity)
    print("uploaded to synapse")

if __name__ == '__main__':
    synId = sys.argv[1]
    uploadLocation = sys.argv[2]
    print(synId)
    print(uploadLocation)
    foo = pull_data(synId)
    foo = run_samtools(foo)
    foo = run_htseq(foo,"/app/gencode.v24.primary_assembly.annotation.gtf")
    foo = push_to_synapse(foo,uploadLocation)
