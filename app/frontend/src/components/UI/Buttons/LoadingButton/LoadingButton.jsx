import React from "react";
import ButtonSpinner from "../../../Spinner/ButtonSpinner/ButtonSpinner";
import Button from "../Button/Button";
import styles from "./LoadingButton.module.css";

const LoadingButton = ({
                           children,
                           isLoading,
                           showChildrenOnLoad = true,
                           dark = false,
                           className,
                           spinnerClassName,
                           ...props
                       }) => {
    const buttonStyles = className ? className : "";

    const spinnerStyles = [spinnerClassName, styles.buttonSpinner];
    if (showChildrenOnLoad) spinnerStyles.push(styles.withChildren);
    if (dark) spinnerStyles.push(styles.darkSpinnerButton);

    return (
        <Button
            className={`${buttonStyles} ${styles.button}`}
            disabled={isLoading && true}
            {...props}
        >
            {isLoading
                ?
                <React.Fragment>
                    <ButtonSpinner className={spinnerStyles.join(" ")}/>
                    {showChildrenOnLoad && children}
                </React.Fragment>
                :
                <React.Fragment>
                    {children}
                </React.Fragment>
            }
        </Button>
    );
};

export default LoadingButton;