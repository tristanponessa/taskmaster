/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   extra3.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/09/26 18:09:36 by trponess          #+#    #+#             */
/*   Updated: 2018/09/30 13:31:59 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

char	**ft_dstrban(char **dstr, char *wanted)
{
	int		i;
	int		k;
	char	**clean;

	i = 0;
	k = 0;
	clean = ft_dstrnew(ft_dstrlen(dstr) - 1, 1);
	while (dstr[i])
	{
		if (!ft_strequ(stock_word_from_str(dstr[i][0], '=', dstr[i]), wanted))
		{
			clean[k] = ft_strjoin(clean[k], dstr[i]);
			k++;
		}
		i++;
	}
	return (clean);
}
