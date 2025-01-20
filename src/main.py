import download_ncbi as dn


def main():
    id_lst = dn.retrieve_accession_by_taxid(taxid='666', page_max=20)
    print(f'{id_lst}\n{len(id_lst)}')


if __name__ == '__main__':
    main()

