#!/bin/bash

# Default values
ACTIVE_WINGDEBUG=False
SLEEP=20
WORKERS=1
MAX_FAILS=1
PUSH=true
PUSH_ATTEMPTS=10
PATTERNS="m08 m07 m06 m05 m04 m03 m02 m01 m00"
PATTERNS=" m01 m00"

# -------------------------------------------------------------------
# pytest handler
# -------------------------------------------------------------------
function handler_pytest(){

  # Start testing
  echo $'\e[1;34m'
  echo "============================================================================="
  echo "Passing all test in order"
  echo "Starting testing (around 10 min with 2 worker)"
  echo "Workers    : $WORKERS"
  echo "Sleep      : $SLEEP"
  echo "Max Fails  : $MAX_FAILS"
  echo "Patterns   : $PATTERNS"
  echo "Debug      : $ACTIVE_WINGDEBUG"
  date
  echo "============================================================================="
  echo $'\e[0m'


  # For each pattern ...
  for patt in $PATTERNS
  do
      count=2 # +1 cycles as is zero based
      passed=false
      while [[ "$passed" == "false" && $count -ge 0 ]]
      do
        echo "passed: $passed, count: $count"

        echo -n $'\e[1;35m'
        echo -n "============================================================================="
        echo $'\e[0m'
        echo "Testing: "$'\e[1;35m'${patt}$'\e[0m'
        date
        # echo $'\e[1;35m'=======================================================$'\e[0m'
        echo -n $'\e[1;35m'
        echo -n "============================================================================="
        echo $'\e[0m'

        pytest -n $WORKERS --maxfail=$MAX_FAILS -k $patt
        exit_code=$?
        echo -n "pytest exit code: "
        echo -n $'\e[1;34m'
        echo -n "$exit_code"
        echo $'\e[0m'


        if [ $exit_code -eq 0 ]; then
            passed=true
            echo $'\e[1;32m'"pytest has passed"$'\e[0m'
        elif [ $exit_code -eq 5 ]; then
            passed=true
            echo $'\e[1;33m'"pytest could't find any test. Continue"$'\e[0m'
        else
            echo $'\e[1;31m'"[count: $count] pytest has failed, SLEEP in $SLEEP seconds"$'\e[0m'
            sleep $SLEEP
          ((count--)) 
        fi
    done
  done

  if [ "$passed" == "true" ]; then
    echo -n $'\e[1;32m'
    echo "Passed: $passed"
    echo $'\e[0m'
  else
    echo -n $'\e[1;31m'
    echo "Passed: $passed"
    echo "Exiting with 1 to stop CI/CD pipelines"$'\e[0m'
    echo $'\e[0m'
    exit 1
  fi
}
# -------------------------------------------------------------------
# push handler
# -------------------------------------------------------------------
function handler_push(){

  # Start testing
  echo $'\e[1;34m'
  echo "============================================================================="
  echo "Trying to push to git safely"
  echo "Passing all test in order before pushing to git"
  echo "Starting testing (around 10 min with 2 worker)"
  echo "Workers    : $WORKERS"
  echo "Sleep      : $SLEEP"
  echo "Max Fails  : $MAX_FAILS"
  echo "Patterns   : $PATTERNS"
  echo "Debug      : $ACTIVE_WINGDEBUG"
  echo "Push       : $PUSH"
  date
  echo "============================================================================="
  echo $'\e[0m'

  # For each pattern ...
  for patt in $PATTERNS
  do
      passed=0
      while [[ $passed -le 0 ]]
      do
        passed=1

        echo -n $'\e[1;35m'
        echo -n "============================================================================="
        echo $'\e[0m'
        echo "Testing: "$'\e[1;35m'${patt}$'\e[0m'
        date
        # echo $'\e[1;35m'=======================================================$'\e[0m'
        echo -n $'\e[1;35m'
        echo -n "============================================================================="
        echo $'\e[0m'
        
        black .

        pytest -n $WORKERS --maxfail=$MAX_FAILS -k $patt
        # https://docs.pytest.org/en/stable/reference/exit-codes.html
        if [ $? -ne 0 ]; then
          echo $'\e[1;31m'"pytest has failed, retry in $SLEEP seconds"$'\e[0m'
          sleep $SLEEP
          passed=0
        fi
    done
  done

  # Test finished
  echo $'\e[1;32m'"All test has been passed"$'\e[0m'
  date
  # Push to git if enabled
  if [ "$PUSH" == "true" ]; then
    attempt=0
    while [ "$((attempt+=1))" -le "$PUSH_ATTEMPTS" ]
    do
      echo $'\e[1;35m'">> [$attempt] Pushing to git"$'\e[0m'
      if git push 
      then
          echo $'\e[1;32m'"Git push successful"$'\e[0m'
          break
      else
          echo $'\e[1;31m'"[${attempt}/${PUSH_ATTEMPTS}] Git push Failed, Retry in $SLEEP seconds"$'\e[0m'
          sleep $SLEEP
      fi
    done
  else
    echo "Skipping pushing to Git"
  fi

}


# -------------------------------------------------------------------
# foo handler
# -------------------------------------------------------------------
function handler_foo(){
  echo "foo is running!"

    count=3
    passed=false

    while [[ "$passed" == "false" && $count -ge 0 ]]
    do
        echo "passed: $passed, count: $count"
        ((count--))
        sleep 1
        
        # Change the passed variable after some iterations
        passed=true
    done

}

# -------------------------------------------------------------------
# Try to find the handler, push by default
# -------------------------------------------------------------------

if [ "$#" -gt 0 ]; then
  HANDLER=$1; shift 1;
else
  HANDLER="pytest";
fi


# -------------------------------------------------------------------
# Analyze options
# -------------------------------------------------------------------

while [ "$#" -gt 0 ]; do
  echo "Parsing: $1"
  case $1 in
    -n) WORKERS="$2"; shift 2;;
    --workers=*) WORKERS="${i#*=}" shift 1;;

    -s) SLEEP="$2"; shift 2;;
    --sleep=*) SLEEP="${i#*=}" shift 1;;

    -f) MAX_FAILS="$2"; shift 2;;
    --fails=*) MAX_FAILS="${i#*=}" shift 1;;

    -s) SLEEP="$2"; shift 2;;
    --sleep=*) SLEEP="${i#*=}" shift 1;;

    -d) ACTIVE_WINGDEBUG="$2"; shift 2;;
    --debug=*) ACTIVE_WINGDEBUG="${i#*=}" shift 1;;

    -k) PATTERNS="$2"; shift 2;;
    --pattern=*) PATTERNS="${i#*=}" shift 1;;

    -a) PUSH_ATTEMPTS="$2"; shift 2;;
    --attempts=*) PUSH_ATTEMPTS="${i#*=}" shift 1;;

    -p) PUSH="$2"; shift 2;;
    --push=*) PUSH="${i#*=}" shift 1;;

    -*) echo "unknown option: $1" >&2; exit 1;;

    *)
    # unknown option
    echo 'Bad argument "$1"'
    shift 1
    ;;
  esac
done


# export WINGDEBUG variable
export ACTIVE_WINGDEBUG


method="handler_$HANDLER"

echo "HANDLER: $HANDLER"
echo "CALLING: $method"
$method "$@"

echo "End"
# handler_pytest
