/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   extra.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/17 18:08:13 by trponess          #+#    #+#             */
/*   Updated: 2018/10/09 12:55:16 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

int		ft_strfind_chs(char *str, char *chs)
{
	int i;
	int j;

	i = 0;
	j = 0;
	while (str[i])
	{
		if (str[i] == chs[j])
		{
			i = -1;
			j++;
			ft_printf("found %c\n", str[i]);
		}
		i++;
	}
	return (j);
}

char	*ft_strjoin_multi(char *s1, char *s2, char *s3, char *s4)
{
	char *str;

	if (!s1 || !s2 || !s3 || !s4)
	{
		ft_printf("ft_strjoin_multi >> dont use NULL\n\n\n");
		return (NULL);
	}
	str = ft_strnew(ft_strlen(s1) + ft_strlen(s2) +
	ft_strlen(s3) + ft_strlen(s4));
	str = ft_strjoin(str, s1);
	str = ft_strjoin(str, s2);
	str = ft_strjoin(str, s3);
	str = ft_strjoin(str, s4);
	return (str);
}

char	*stock_word_from_str(char from_ch1, char to_ch2, char *str)
{
	char	*word;
	int		i;
	int		j;

	i = 0;
	j = 0;
	if (ft_strfind(str, to_ch2) == 0)
		return (NULL);
	word = ft_strnew(ft_strlen(str));
	while (from_ch1 != -1 && str[j] != from_ch1)
		j++;
	while (str[j] != to_ch2)
	{
		word[i] = str[j];
		i++;
		j++;
	}
	word[i] = '\0';
	return (word);
}

char	*ft_stradd(char *str, int n)
{
	char *new;

	new = ft_strnew(ft_strlen(str) + n);
	ft_strcpy(new, str);
	return (new);
}

char	**ft_strict_dstr(char **tab)
{
	int i;

	i = 0;
	while (tab[i])
	{
		if (ft_strlen(tab[i]) == 0)
		{
			tab[i] = 0;
			return (tab);
		}
		i++;
	}
	return (tab);
}
