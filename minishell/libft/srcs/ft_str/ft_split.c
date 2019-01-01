/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/07/22 16:10:59 by trponess          #+#    #+#             */
/*   Updated: 2018/09/26 16:37:53 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		find_nb_words(char *str, char sep)
{
	int i;
	int nb;

	i = 0;
	nb = 0;
	while (str[i])
	{
		if (str[i] != sep && (str[i + 1] == sep || str[i + 1] == '\0'))
			nb++;
		i++;
	}
	return (nb);
}

char	**ft_split_spaces(char *str, char sep)
{
	char	**tab;
	int		i;
	int		j;
	int		k;

	i = 0;
	j = 0;
	k = 0;
	tab = NULL;
	tab = ft_dstrnew(find_nb_words(str, sep), ft_strlen(str));
	while (str[i])
	{
		while (str[i] == sep)
			i++;
		while (str[i] && str[i] != sep)
		{
			tab[j][k] = str[i];
			k++;
			i++;
		}
		j++;
		k = 0;
	}
	return (tab);
}

char	**ft_split_most_wanted(char *str, char **sep, char rep, char *safehouse)
{
	char **tab;
	char *clean_str;

	clean_str = str_most_wanted_p(str, sep, rep, safehouse);
	tab = ft_split_spaces(clean_str, rep);
	return (tab);
}
