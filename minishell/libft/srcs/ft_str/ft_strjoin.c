/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:19:49 by trponess          #+#    #+#             */
/*   Updated: 2018/10/09 13:02:32 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

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

char			*ft_strjoin(char *s1, char *s2)
{
	char	*word;

	if (!s1 || !s2)
		return (NULL);
	word = ft_strnew(ft_strlen(s1) + ft_strlen(s2));
	return (ft_stock(word, s1, s2));
}

char			**ft_dstrjoin(char **dstr1, char **dstr2)
{
	int		size;
	char	**fusion;
	int		k;
	int		i;

	k = 0;
	if (!dstr1 || !dstr2)
		return (NULL);
	size = ft_dstrlen(dstr1) + ft_dstrlen(dstr2);
	fusion = ft_dstrnew(size, 1);
	i = -1;
	while (dstr1[++i])
	{
		fusion[k] = ft_strnew(ft_strlen(dstr1[i]));
		ft_strcpy(fusion[k++], dstr1[i]);
	}
	i = -1;
	while (dstr2[++i])
	{
		fusion[k] = ft_strnew(ft_strlen(dstr2[i]));
		ft_strcpy(fusion[k++], dstr2[i]);
	}
	fusion[k] = 0;
	return (fusion);
}
