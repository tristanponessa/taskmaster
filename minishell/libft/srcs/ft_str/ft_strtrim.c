/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 18:27:19 by trponess          #+#    #+#             */
/*   Updated: 2018/09/27 18:26:36 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

static int		ft_strlen_space(const char *s)
{
	int	i;
	int	n;

	i = 0;
	n = 0;
	while (s[i] == ' ' || s[i] == '\t' || s[i] == '\n')
		i++;
	while (s[i] != '\0')
	{
		n++;
		i++;
	}
	i--;
	if (n > 0)
	{
		while (s[i] == ' ' || s[i] == '\t' || s[i] == '\n')
		{
			i--;
			n--;
		}
	}
	return (n);
}

char			*ft_strtrim(const char *s)
{
	char	*new;
	int		j;
	int		i;
	int		len;

	i = 0;
	j = 0;
	if (!s)
		return (NULL);
	len = ft_strlen_space(s);
	if (!(new = ft_strnew(len + 1)))
		return (NULL);
	while (s[j] == ' ' || s[j] == '\t' || s[j] == '\n')
		j++;
	while (i < len)
	{
		new[i] = s[j + i];
		i++;
	}
	new[i] = '\0';
	return (new);
}
