FTITLE = __file__.split("/", maxsplit=-1)[-1].split(".", maxsplit=-1)[0]

cprint = print


def get_input(prompt: str = "Input", mark: str = ">",
              default: str | None = None,
              choices: list[str] | None = None,
              show_choices: bool = True,
              # 'pass_exc': False,
              # nl: str = "") -> str:
              **kwargs) -> str | None:
    """ Getting text input.

        Args:
            prompt (str, optional): Prompt to display. Defaults to "> ".
            mark (str, optional): Mark to display. Defaults to "> ".
            default (str, optional): Default value. Defaults to "".
            choices (list[str], optional): List of choices. Defaults to None.
            show_choices (bool, optional): If choices are to be displayed.
                Defaults to True.
            pass_exc (bool, optional): If Exception are to be reraised.
            nl (str, optional): Newline character. Defaults to "\n".
    """

    location = FTITLE + ".get_input"

    params = kwargs['params'] if 'params' in kwargs else {'nl': "",
                                                          'pass_exc': False}
    pass_exc = params.get('pass_exc', False)
    nl = params.get('nl', "")
    ans = None
    default_str = f"[{default!s}]" if default else ""
    # prompt = f"{prompt} {tuple(choices)} {mark} " if choices is not None else\
    #     f"{prompt} {mark} "
    if choices is not None:
        assert default in choices or default is None, \
            f"Default value {default!r} not in choices"
        if show_choices:
            choices_txt = f" {tuple(choices)} "
        else:
            choices_txt = ""
        prompt = f"{prompt}{choices_txt}{default_str}{mark} "
    else:
        prompt = f"{prompt} {default_str}{mark} "
    condition = ans not in choices if choices is not None else True

    while condition:
        try:
            # cprintd(f"asking for input…", location=location)
            cprint(f"{prompt}{nl}", end=nl)
            ans = input()
            if ans == "" and default is not None:
                return default

            if choices is not None and ans not in choices:
                # cprint(f"Input should be on of ({', '.join(choices)}), "
                cprint(f"Input should be on of {tuple(choices)}, "
                       f"not {ans!r}.\nTry again or Ctrl-C to abort.")
                continue
            return ans
        except KeyboardInterrupt:
            # cprintd("Inside `except` for: "
            #         f"KeyboardInterrupt, {ans = !r}, {pass_exc = }",
            #         location=location)
            print()
            condition = False
            if pass_exc:
                raise
            print("\b\b  \n …aborted…")


def confirm(prompt, default="y", params: dict = {'nl': ""}):
    """ Getting user confirmation: yes/no, y/n, 1/0, etc. """

    ans_true = ["y", "yes", "ok", "true", "1", "t", "tak", True]
    ans_false = ["n", "no", "nah", "false", "0", "nie", False]
    ans = "[-]"
    # cprintd(f"{default = }", location=FTITLE + ".confirm")
    nl = params.get('nl', "")
    if str(default).lower() in ans_true:
        default = ans_true[0]
    elif str(default).lower() in ans_false:
        default = ans_false[0]
    else:
        ERR = ("Default answer is of incorrect form. Should be one of "
              f"".join([str(ans) for ans in ans_true + ans_false]))
        raise ValueError(ERR)
    while ans not in ans_true + ans_false:
        params = {'nl': nl}
        try:
            ans = get_input(prompt, mark="?", default=default,
                            params=params).lower()
        except AttributeError:
            return False
        if ans not in ans_true + ans_false:
            cprint(f"Incorrect form of the answer.")

    return ans in ans_true
