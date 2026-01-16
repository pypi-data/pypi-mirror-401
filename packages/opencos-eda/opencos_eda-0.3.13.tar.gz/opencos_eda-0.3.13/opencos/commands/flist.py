'''opencos.commands.flist - Base class command handler for: eda flist ...

Intended to be overriden by Tool based classes (such as CommandFListVivado, etc).'''

# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

import os
import shlex

from opencos import util, eda_config
from opencos.eda_base import CommandDesign, Tool
from opencos.utils.str_helpers import strip_all_quotes
from opencos.commands.sim import parameters_dict_get_command_list
from opencos.utils.str_helpers import strip_outer_quotes

class CommandFList(CommandDesign):
    '''Base class command handler for: eda flist ...'''

    command_name = 'flist'

    def __init__(self, config: dict):
        CommandDesign.__init__(self, config=config)

        # If there's no tool attached, then we'll assume this flist is being created
        # to run in `eda`, not some vendor tool.
        self.flist_has_tool = isinstance(self, Tool)

        self.flist_args = {
            'out'                : "flist.out",
            'emit-define'        : True,
            'emit-parameter'     : True,
            'emit-incdir'        : True,
            'emit-plusargs'      : True,
            'emit-v'             : True,
            'emit-sv'            : True,
            'emit-vhd'           : True,
            'emit-cpp'           : True,
            'emit-non-sources'   : True, # as comments, from DEPS 'reqs'
            'emit-eda-args'      : not self.flist_has_tool, # no Tool means flist for eda.
            'prefix-define'      : "+define+",
            'prefix-parameter'   : "-G",
            'prefix-incdir'      : "+incdir+",
            'prefix-plusargs'    : "+",
            'prefix-v'           : "",
            'prefix-sv'          : "",
            'prefix-vhd'         : "",
            'prefix-cpp'         : "",
            'prefix-non-sources' : "", # as comments anyway.
            # NOTE - the defaults are for creating an flist that is suitable for 'eda', which for
            # defines means: optionally single-quote the entire thing, double-quote string values
            # only.
            # Tool classes should override if they want to set safe-mode-defines=True.
            # Tool classes may also avoid these args entirely in their derived CommandFList class
            'safe-mode-defines'   : not self.flist_has_tool, # no Tool
            'bracket-quote-define': False,
            'single-quote-define': False,
            'quote-define'       : self.flist_has_tool, # Tool, this is NOT for eda.
            'equal-define'       : True,
            'escape-define-value': False,
            'quote-define-value' : False,
            'bracket-quote-path' : False,
            'single-quote-path'  : False,
            'double-quote-path'  : False,
            'quote-path'         : True,
            'build-script'       : "", # we don't want this to error either

            'print-to-stdout': False,

            # ex: eda flist --print-to-stdout --emit-rel-path --quiet <target>
            'emit-rel-path'  : False,
        }


        self.args.update({
            'eda-dir'            : 'eda.flist', # user can specify eda-dir if files are generated.
        })
        self.args.update(self.flist_args)

        self.args_help.update({
            'print-to-stdout': "do not save file, print to stdout",
        })

    def process_tokens(
            self, tokens: list , process_all: bool = True, pwd: str = os.getcwd()
    ) -> list:
        unparsed = CommandDesign.process_tokens(
            self, tokens=tokens, process_all=process_all, pwd=pwd
        )
        if self.stop_process_tokens_before_do_it():
            return unparsed

        self.do_it()
        return unparsed

    def get_flist_dict(self) -> dict:
        '''Returns dict of some internal class member vars, ignores args

        Useful for an external caller to get details about this CommandDesign child
        object without generating a .f file, or having to know specifics about the
        class
        '''
        self.command_safe_set_tool_defines() # (Command.command_safe_set_tool_defines)

        ret = {}
        for key in ['files_sv', 'files_v', 'files_vhd', 'defines', 'incdirs',
                    'parameters', 'unprocessed-plusargs']:
            # These keys must exist, all are lists, defines is a dict
            x = getattr(self, key, None)
            if isinstance(x, (dict, list)):
                ret[key] = x.copy()
            else:
                ret[key] = x
        return ret

    def get_flist_defines_list(self) -> list:
        '''Returns formatted list of str for known defines'''

        ret = []
        prefix = strip_all_quotes(self.args['prefix-define'])
        for d, value in self.defines.items():

            if value is None:
                ret.append(prefix + d)
                continue

            # else, value exists:
            safe_mode_guard_str_value = bool(
                self.args['safe-mode-defines'] and isinstance(value, str) and ' ' in value
            )

            if self.args['bracket-quote-define']:
                qd1 = "{"
                qd2 = "}"
            elif self.args['single-quote-define']:
                qd1 = "'"
                qd2 = "'"
            elif self.args['quote-define']:
                qd1 = '"'
                qd2 = '"'
            else:
                qd1 = ''
                qd2 = ''

            if self.args['equal-define']:
                ed1 = '='
            else:
                ed1 = ' '

            if self.args['escape-define-value']:
                value = value.replace('\\', '\\\\').replace('"', '\\"')
            if self.args['quote-define-value']:
                value = '"' + value + '"'
            if safe_mode_guard_str_value:
                value = strip_outer_quotes(value.strip('\n'))
                value = '"' + value + '"'

            if self.args['quote-define'] and value.startswith('"') and value.endswith('"'):
                # If you wanted your define to look like:
                # +define+"NAME=VALUE", but VALUE also has double quotes wrapping it,
                # it's unlikely to work so we'll optimistically so escape the " wrapping value.
                # If you have additional " in the middle of the value, good luck.
                value = '\\"' + value[1:-1] + '\\"'

            newline = prefix + qd1 + f"{d}{ed1}{value}" + qd2

            if safe_mode_guard_str_value:
                # wrap the entire thing with single-quotes, so it survives as a single
                # token in an eda dot-f file:
                newline = shlex.quote(newline)

            ret.append(newline)

        return ret

    def get_flist_plusargs_list(self) -> list:
        '''Returns formatted list of str for unprocessed plusargs

        Tool based classes can override if they also want to query their own
        processed plusargs, such as CommandSim.args[sim-plusargs']
        '''
        ret = []
        for x in self.args.get('unprocessed-plusargs', []) + self.args.get('sim-plusargs', []):
            if self.args['prefix-plusargs']:
                if x.startswith('+'):
                    x = x[1:] # strip leading +
                x = self.args['prefix-plusargs'] + x
            ret.append(x)
        return ret

    def get_flist_parameter_list(self) -> list:
        '''Returns formatted list of str for parameters'''
        prefix = strip_all_quotes(self.args['prefix-parameter'])
        return parameters_dict_get_command_list(
                params=self.parameters, arg_prefix=prefix, for_flist=True
        )

    def get_flist_eda_args_list(self) -> list:
        '''Returns list of eda args for an eda-capable flist

        - This will NOT add any util based args (--color | --no-color, --debug, etc)
        - This will NOT add any -f/--input-file args (those are already resolved)

        - This WILL add --env-file args
        - This WILL add --config-yml args that were not default value

        Not intended to be overriden by Tool based command classes.
        '''
        ret = []

        # --env-file(s), if used:
        for env_file in util.env_files_loaded:
            ret.append(f'--env-file={env_file}')

        # --config-yml, if non-default:
        ret.extend(eda_config.get_config_yml_args_for_flist())

        # EDA args, but not the flist specific args, and only those that were modified.
        for arg, _ in self.modified_args.items():

            if arg in self.flist_args:
                # do not emit flist command args
                continue

            value = self.args[arg]
            if isinstance(value, bool):
                if value:
                    ret.append(f'--{arg}')
                else:
                    ret.append(f'--no-{arg}')
            else:
                ret.append(f'--{arg}={value}')
        return ret

    def get_additional_flist_args_list(self) -> list:
        '''Derived classes may override, to output additional args in the flist'''
        return []

    def get_additional_flist_files_list(self) -> list:
        '''Derived classes may override, to output additional files in the flist'''
        return []


    def do_it(self) -> None:
        '''do_it() is the main entry point for creating the flist(),

        Usually it is called from self.process_tokens()'''

        # add defines for this job
        self.command_safe_set_tool_defines() # (Command.command_safe_set_tool_defines)

        if not self.args['top']:
            util.warning(f'CommandFList: {self.command_name=} not run due to lack of',
                         f'{self.args["top"]=} value')
            self.write_eda_config_and_args()
            return

        if self.config['tool']:
            tool_string = f' (with --tool={self.config["tool"]})'
        else:
            tool_string = ''

        # if config['tool'] is set, but self.flist_has_tool is False, we're likely using
        # this default handler CommandFList and the Tool class hasn't defined what they
        # do. In this case, simply warn that this will emit a non-tool specific default flist
        # intended for use by `eda`:
        if self.config['tool'] and not self.flist_has_tool:
            util.warning(f'For command="flist"{tool_string}, there is no tool',
                         'specific handler for producing an flist. The default eda flist will',
                         'be emitted')
            # If this happens, you'll likely want the Tool based defines (that were never set
            # by Tool.set_tool_defines(self) b/c we have no Tool class.
            # TODO(drew): This is only a best-effort, we could create a derived Tool object and
            # instead call obj.set_tool_defines(), and update self.defines instead?
            _tool_config = self.config.get('tools', {}).get(self.config['tool'], {})
            self.defines.update(
                _tool_config.get('defines', {})
            )



        # check if we're overwriting the output flist file.
        if self.args['print-to-stdout']:
            pass
        elif os.path.exists(self.args['out']):
            if self.args['force']:
                util.info(f"Removing existing {self.args['out']}")
                os.remove(self.args['out'])
            else:
                self.error(f"Not overwriting {self.args['out']} unless you specify --force")

        # Note - we create a work_dir in case any DEPS commands created files that need to be
        # added to our sources.
        self.create_work_dir()
        self.run_dep_commands()

        pq1 = ""
        pq2 = "" # pq = path quote
        if not self.args['quote-path']:
            pass # if we decide to make one of the below default, this will override
        elif self.args['bracket-quote-path']:
            pq1 = "{"
            pq2 = "}"
        elif self.args['single-quote-path']:
            pq1 = "'"
            pq2 = "'"
        elif self.args['double-quote-path']:
            pq1 = '"'
            pq2 = '"'

        if self.args['print-to-stdout']:
            fo = None
            print()
        else:
            util.debug(f"Opening {self.args['out']} for writing")
            fo = open( # pylint: disable=consider-using-with
                self.args['out'], 'w', encoding='utf-8'
            )
            print(f"## {self.args=}", file=fo)

            if self.args['emit-non-sources']:
                if self.files_non_source:
                    print('## reqs (non-source files that are dependencies):', file=fo)
                    prefix = strip_all_quotes(self.args['prefix-non-sources'])
                    for f in self.files_non_source:
                        if self.args['emit-rel-path']:
                            f = os.path.relpath(f)
                        print('##    ' + prefix + pq1 + f + pq2, file=fo)

        if self.args['emit-eda-args']:
            for newline in self.get_flist_eda_args_list():
                print(newline, file=fo)

        defines_lines = self.get_flist_defines_list()
        if not self.args['emit-define'] and defines_lines:
            util.warning(f'Command "flist"{tool_string}, has defines present but they were not',
                         f'included in the output flist: {defines_lines}')

        parameter_lines = self.get_flist_parameter_list()
        if not self.args['emit-parameter'] and parameter_lines:
            util.warning(f'Command "flist"{tool_string}, has parameters present but they were not',
                         f'included in the output flist: {parameter_lines}')

        plusarg_lines = self.get_flist_plusargs_list()
        if not self.args['emit-plusargs'] and plusarg_lines:
            util.warning(f'Command "flist"{tool_string}, has plusargs present but they were not',
                         f'included in the output flist: {plusarg_lines}')

        if self.args['emit-define']:
            for newline in defines_lines:
                print(newline, file=fo)

        if self.args['emit-parameter']:
            for newline in parameter_lines:
                print(newline, file=fo)


        if self.args['emit-incdir']:
            prefix = strip_all_quotes(self.args['prefix-incdir'])
            for i in self.incdirs:
                if self.args['emit-rel-path']:
                    i = os.path.relpath(i)
                print(prefix + pq1 + i + pq2, file=fo)

        if self.args['emit-plusargs']:
            for newline in plusarg_lines:
                print(newline, file=fo)


        # Hook for derived classes to optionally print additional custom args, prior to
        # any files:
        for newline in self.get_additional_flist_args_list():
            print(newline, file=fo)

        if self.args['emit-v']:
            prefix = strip_all_quotes(self.args['prefix-v'])
            for f in self.files_v:
                if self.args['emit-rel-path']:
                    f = os.path.relpath(f)
                print(prefix + pq1 + f + pq2, file=fo)

        if self.args['emit-sv']:
            prefix = strip_all_quotes(self.args['prefix-sv'])
            for f in self.files_sv:
                if self.args['emit-rel-path']:
                    f = os.path.relpath(f)
                print(prefix + pq1 + f + pq2, file=fo)
        if self.args['emit-vhd']:
            prefix = strip_all_quotes(self.args['prefix-vhd'])
            for f in self.files_vhd:
                if self.args['emit-rel-path']:
                    f = os.path.relpath(f)
                print(prefix + pq1 + f + pq2, file=fo)
        if self.args['emit-cpp']:
            prefix = strip_all_quotes(self.args['prefix-cpp'])
            for f in self.files_cpp:
                if self.args['emit-rel-path']:
                    f = os.path.relpath(f)
                print(prefix + pq1 + f + pq2, file=fo)

        # Hook for derived classes to optionally print additional flist items after
        # any files:
        for newline in self.get_additional_flist_files_list():
            print(newline, file=fo)

        if self.args['print-to-stdout']:
            print() # don't need to close fo (None)
        else:
            fo.close()
            util.info(f"Created file: {self.args['out']}")

        self.write_eda_config_and_args()
        self.run_post_tool_dep_commands()
