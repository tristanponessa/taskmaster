/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/06/28 19:13:46 by tristan           #+#    #+#             */
/*   Updated: 2018/10/04 17:01:40 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft/includes/libft.h"
#include "../minishell.h"

int		main(int ac, char **av, char **ev)
{
	char **ev_cp;

	ft_use_args(ac, av, NULL);
	showoff(2);
	showoff(1);
	if (ft_dstrlen(ev) == 0)
	{
		ft_printf("error : empty env\n");
		return (0);
	}
	ev_cp = ft_split_spaces(&ev[look_for_envvar(ev, "PATH")][5], ':');
	save(ev, NULL, 1);
	shell_runs(ev, ev_cp);
	return (0);
}
