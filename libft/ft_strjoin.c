/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:19:49 by trponess          #+#    #+#             */
/*   Updated: 2017/11/24 13:03:37 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static char		*ft_stock(char *word, char *s1, char *s2)
{
	int i;
	int j;

	i = 0;
	j = 0;
	while (s1[j])
	{
		word[i] = s1[j];
		i++;
		j++;
	}
	j = 0;
	while (s2[j])
	{
		word[i] = s2[j];
		i++;
		j++;
	}
	word[i] = '\0';
	return (word);
}

char			*ft_strjoin(char const *s1, char const *s2)
{
	char	*word;

	if (!s1 || !s2)
		return (NULL);
	if (!(word = (char *)malloc(sizeof(char) * (ft_strlen((char *)s1)
		+ ft_strlen((char *)s2) + 1))))
		return (NULL);
	return (ft_stock(word, (char *)s1, (char *)s2));
}
