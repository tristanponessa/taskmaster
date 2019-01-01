/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   minishell.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/08 21:06:44 by tristan           #+#    #+#             */
/*   Updated: 2018/09/29 18:54:55 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef MINISHELL_H
# define MINISHELL_H

# include "libft/includes/libft.h"
# include <dirent.h>
# include <sys/types.h>
# include <sys/stat.h>
# include <unistd.h>
# include <time.h>
# include <grp.h>
# include <pwd.h>
# include <sys/xattr.h>
# include <sys/types.h>
# include <sys/wait.h>

void	minishell(void);
int		build_in(char *command, char **args, char ***env);
void	ft_echo(char **args);
char	**ft_setenv(char **env, char **args);
char	**ft_unsetenv(char **env, char **args);
char	**ft_resetenv(char **env, char **original_env, char **args);
void	ft_man(char *command);
char	**ft_cd(char **env, char **args);
void	ft_env(char **env, char **args);
void	ft_man(char *command);
char	*modify(char *env, char **args);
char	**add(char **env, int i, char **args);
void	ft_free();
void	end_str(char *str, int *i);
int		ft_strlen_upto(char *str, char ch);
int		ft_strequ_upto(char *s1, char *s2, char ch);
int		ft_strfind_chs(char *str, char *chs);
char	*find_parent(char *path);
char	*ft_strjoin_all(char **strs);
char	*ft_strjoin_multi(char *s1, char *s2, char *s3, char *s4);
char	*stock_word_from_str(char from_ch1, char to_ch2, char *str);
char	*ft_strcpy_after(char *dest, char *src, char ch);
char	*ft_strcpy_upto(char *dest, char *src, char ch);
char	*ft_stradd(char *str, int n);
char	**save(char **env, char **args, int save);
char	**ft_strict_dstr(char **tab);
char	*ft_strcpy_after(char *dest, char *src, char ch);
char	*ft_strcpy_upto(char *dest, char *src, char ch);
int		ft_strequ_upto(char *s1, char *s2, char ch);
void	showoff(int i);
void	shell_runs(char **ev, char **ev_paths);
void	create_process(char *dir, char **args, char **ev);
int		look_for_envvar(char **env, char *str);
char	*search_for_command(char *command, char **env_paths);
char	*ft_getcwd();
char	*add_to_path(char *path, char *rest);
char	*find_parent(char *path);
char	*ft_getcwd();
char	**fill_ev(char **ev);
char	**translate_av(char **env, char **original_env, char **args);
char	**prepare_args();
char	**save(char **env, char **args, int save);
char	*translate_var(char **env, char *args);
char	**if_pwds_empty(char **env, char **original_env);
char	*double_period_pattern(char *args);
char	*dstr_to_str(char **dstr, char *sep);
void	translate_path(char **env, char **part, int *o);
char	*find_path(char **env, char **part);
char	**ft_dstrban(char **dstr, char *wanted);

#endif
