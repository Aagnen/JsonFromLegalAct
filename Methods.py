import pypdf
import re

# ---------------------------------------- METHODS --------------------------------------------------#


def split_all(text_string):
    art_dict_out = split_to_art(text_string)
    art_ust_dict_out = split_to_ustepy(art_dict_out)
    art_ust_pdp_dict = split_to_podpunkty(art_ust_dict_out)
    return art_ust_pdp_dict


def split_to_art(text_string):
    art_dict = {}
    all_art_list = [u for x in text_string.split('Art.') for u in (x, 'Art.')]
    for i in range(0, len(all_art_list)-1):
        if all_art_list[i] == 'Art.':
            this_art = all_art_list[i+1]
            this_art_split = this_art.split('.')
            this_art_number = this_art_split[0]
            this_art_clear_list = this_art_split[1:len(this_art_split)]
            this_art_clear_str = ".".join(this_art_clear_list)

            art_dict[f'Art.{this_art_number}'] = f'\n{this_art_clear_str}'
    return art_dict


def split_to_ustepy(art_dictionary):
    art_ust_dict = art_dictionary

    # For every article
    for art_key in art_dictionary:
        ust_dict = {}
        artykul_all = art_dictionary[art_key]

        artykul_split = re.split('((\n)\s*\d{1,4}[a-z]{,3}[.])', artykul_all)
        # print(f'{art_key}: {artykul_split}')

        # For every ust
        new_ust_number = " 0"
        for i in range(0, len(artykul_split)):
            if re.match('((\n)\s*\d{1,4}[a-z]{,3}[.])', artykul_split[i]):
                new_ust_number = artykul_split[i].replace('.', '').replace(' ', '').replace('\n', '')
                continue

            if artykul_split[i] != " " and artykul_split[i] != "\n" and artykul_split[i] != "":
                ust_dict[f'ust.{new_ust_number}'] = artykul_split[i]
            # ust_dict[f'ust.{i}'] = artykul_split[i]

        art_ust_dict[art_key] = ust_dict

    return art_ust_dict


def split_to_podpunkty(art_ust_dictionary):
    art_ust_pd_dict = art_ust_dictionary

    # For every article
    for art_key in art_ust_dictionary:
        ust_pd_dict = {}
        this_ust = art_ust_dictionary[art_key]

        # For every ust
        for ust_key in this_ust:
            pd_dict = {}
            ust_all = this_ust[ust_key]

            ust_split = re.split('((\n)\s*\d{1,4}[a-z]{,3}[)])', ust_all)

            # For every pdp
            new_pdp_number = " 0"
            for i in range(0, len(ust_split)):
                if re.match('((\n)\s*\d{1,4}[a-z]{,3}[)])', ust_split[i]):
                    new_pdp_number = ust_split[i].replace(')', '').replace(' ', '').replace('\n', '')
                    continue

                if ust_split[i] != " " and ust_split[i] != "\n" and ust_split[i] != "":
                    pd_dict[f'pdp.{new_pdp_number}'] = ust_split[i]

            ust_pd_dict[ust_key] = pd_dict
        art_ust_pd_dict[art_key] = ust_pd_dict

    return art_ust_pd_dict

