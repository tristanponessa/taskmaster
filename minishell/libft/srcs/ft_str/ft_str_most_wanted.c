/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_most_wanted.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tristan <tristan@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/07/22 16:09:02 by trponess          #+#    #+#             */
/*   Updated: 2018/09/25 21:37:49 by tristan          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*str_most_wanted_p(char *str, char **sep, char ch, char *safehouse)
{
	int i;
	int j;
	int wanted;

	wanted = 1;
	j = -1;
	while (sep[++j])
	{
		i = -1;
		while (str[++i])
		{
			if (str[i] == safehouse[1] && wanted == 0)
				wanted = 1;
			else if (str[i] == safehouse[0] && wanted == 1)
				wanted = 0;
			else if (ft_strncmp(sep[j], &str[i], ft_strlen(sep[j])) == 0 &&
					wanted == 1)
				ft_memset(&str[i], ch, ft_strlen(sep[j]));
		}
	}
	i = 0;
	while (str[i++])
		if (str[i] == safehouse[0] || str[i] == safehouse[1])
			str[i] = ch;
	return (str);
}
