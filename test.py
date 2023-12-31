import os
import project1 as Main

class Tester:
  @staticmethod
  def formatTestResult(result):
    if result:
      return "Pass"
    return "Fail"

  @staticmethod
  def testGameHasEnded():
    with open('game_end', "w") as file:
      file.write("Test case!")
    print(f'gameHasEnded(): {Tester.formatTestResult(Main.gameHasEnded())}')
    if os.path.exists('game_end'):
      os.remove('game_end')

  @staticmethod
  def runTests():
    Tester.testGameHasEnded()