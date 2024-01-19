from env_simulator.environment import Environment, EnvironmentFactory


# Initialize the simulation environment

env = EnvironmentFactory.create_environment('/Users/stefan/Work/Pyenvs/Yukinoaru/data/nuvei_env.json')

env.run_simulation()
