/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strsplit.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/07/18 11:42:26 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:04:25 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static char		**ft_create_tab(char *str, int nb_word, int len_word, char c)
{
	char	**tab;
	int		i;
	int		j;
	int		k;

	tab = (char**)malloc(sizeof(*tab) * nb_word + 1);
	if (!str || !tab)
		return (NULL);
	i = 0;
	j = 0;
	while (j < nb_word && str[i])
	{
		k = 0;
		tab[j] = (char*)malloc(sizeof(**tab) * len_word + 1);
		if (!tab[j])
			return (NULL);
		while (str[i] == c && str[i])
			i++;
		while (str[i] != c && str[i])
			tab[j][k++] = str[i++];
		tab[j++][k] = '\0';
	}
	tab[j] = 0;
	return (tab);
}

char			**ft_strsplit(char const *s, char c)
{
	int		nb_word;
	int		len_word;
	int		max_len_word;
	int		i;

	if (!s)
		return (NULL);
	nb_word = 0;
	max_len_word = 0;
	i = 0;
	while (s[i++])
	{
		len_word = 0;
		while (s[i] == c && s[i])
			i++;
		if (s[i] != c && s[i])
		{
			nb_word++;
			while (s[i] != c && s[i++])
				len_word++;
			if (len_word > max_len_word)
				max_len_word = len_word;
		}
	}
	return (ft_create_tab((char *)s, nb_word, max_len_word, c));
}
