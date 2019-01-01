/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   extra2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/20 11:29:01 by trponess          #+#    #+#             */
/*   Updated: 2018/09/24 18:00:09 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

void	end_str(char *str, int *i)
{
	*i = ft_strlen(str) - 1;
}

int		ft_strlen_upto(char *str, char ch)
{
	int i;

	i = 0;
	while (str[i] && str[i] != ch)
		i++;
	return (i);
}

int		ft_strequ_upto(char *s1, char *s2, char ch)
{
	int		i;

	i = 0;
	if (!s1 || !s2)
		return (0);
	if (!ft_strfind(s2, ch))
		ft_printf("error : ft_strequ_upto -> s2 must contain ch\n\n\n");
	while (s1[i] && s2[i] && s1[i] == s2[i] && s1[i] != ch)
		i++;
	i--;
	if (i < 0)
		i = 0;
	if (s1[i] == s2[i] && ft_strlen_upto(s1, '=') == ft_strlen(s2))
		return (1);
	return (0);
}

char	*ft_strcpy_upto(char *dest, char *src, char ch)
{
	int i;

	i = 0;
	if (!dest || !src)
		return (NULL);
	while (src[i] && src[i] != ch)
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

char	*ft_strjoin_all(char **strs)
{
	char	*sentence;
	int		i;
	int		size;

	i = 0;
	size = 0;
	while (strs[++i])
		size += ft_strlen(strs[i]);
	sentence = ft_strnew(size);
	i = 0;
	while (strs[++i])
		sentence = ft_strjoin(sentence, strs[i]);
	return (sentence);
}
