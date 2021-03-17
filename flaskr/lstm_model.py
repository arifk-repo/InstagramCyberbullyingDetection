import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM, SpatialDropout1D, Dropout
import tensorflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model
import tensorflow as tf
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import KFold
from . import admin
import os
from keras.callbacks import CSVLogger


class LstmModel:
    max_features = 5000
    batch_size = 128
    path = "flaskr"
    basepath_model = os.path.join(path, "data", "model", "prediksi.h5")
    basepath_token = os.path.join(path, "data", "tokenizer", "tokenizer.pickle")
    basepath_matrix = os.path.join(path, "data", "matrix", "maximums3.npy")
    basepath_history = os.path.join(path, "data", "matrix", "history_model.npy")
    basepath_confusion = os.path.join(path, "data", "confusion", "confusion_matrix.csv")
    normal = admin.Activate()

    def __init__(self, dataframe):
        self.train_data = dataframe
        self.data_scrape = []

    def __repr__(self):
        return f"Lstm Model for cyberbullying identification"

    def tokenize_data(self):
        global tokenizer
        global X
        global Y
        global X_train, X_test, Y_train, Y_test
        global vocab_size
        tokenizer = Tokenizer(num_words=self.max_features, split=' ')
        tokenizer.fit_on_texts(self.train_data['after_prepro'].values)
        X = tokenizer.texts_to_sequences(self.train_data['after_prepro'].values)
        X = pad_sequences(X)
        Y = pd.get_dummies(self.train_data['score']).values
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=32, shuffle=True)
        with open(self.basepath_token, 'wb') as handle:
            pickle.dump(tokenizer, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)
        vocab_size = len(tokenizer.word_index)+1

    def make_model(self):
        embedding_matrix=np.load(self.basepath_matrix)
        embed_dim = 128
        lstm_out = 64
        model = tensorflow.keras.Sequential()
        model.add(Embedding(vocab_size, embed_dim, weights=[embedding_matrix], input_length=50, trainable=True))
        model.add(SpatialDropout1D(0.25))
        model.add(LSTM(lstm_out, dropout=0.3))
        model.add(Dropout(0.2))
        kernel_regularizer = tf.keras.regularizers.L1L2()
        model.add(Dense(4, activation='softmax', kernel_regularizer=kernel_regularizer))
        optimizer = tf.keras.optimizers.Adam()
        model.compile(loss='categorical_crossentropy',
                      optimizer=optimizer, metrics=['accuracy'])
        print(model.summary())
        csv_loger=CSVLogger(os.path.join(self.path, "data", "model", "logger2.csv"),append=True)
        history = model.fit(X_train, Y_train, epochs=100, batch_size=self.batch_size, validation_data=(X_test, Y_test), verbose=1, callbacks=[csv_loger])
        model.save(os.path.join(self.path, "data", "model", "coba2.h5"))
        np.save(self.basepath_history, history.history)

    def load_model(self):
        model = load_model(self.basepath_model)
        Y_pred = model.predict_classes(X_test, batch_size=self.batch_size)
        df_test = pd.DataFrame({'true': Y_test.tolist(), 'pred': Y_pred})
        df_test['true'] = df_test['true'].apply(lambda x: np.argmax(x))
        df_test.to_csv(self.basepath_confusion)
        print("confusion matrix")
        cf=confusion_matrix(df_test.true, df_test.pred)
        print(cf)
        cf_report=pd.DataFrame(cf)
        self.basepath_cf = os.path.join(self.path, "data", "confusion", "cf.csv")
        cf_report.to_csv(self.basepath_cf)
        class_report = classification_report(df_test.true, df_test.pred, output_dict=True)
        print(class_report)
        report = pd.DataFrame(class_report).transpose()
        basepath_report = os.path.join(self.path, "data", "confusion", "report.csv")
        report.to_csv(basepath_report)

    def kfold_cross(self):
        embedding_matrix = np.load(self.basepath_matrix)
        n_split = 10
        i = 0
        batch_size = 128
        accuracy_model = []
        f1_model = []
        precission_model = []
        recall_model = []
        for train_index, test_index in KFold(n_split, shuffle=True).split(X):
            i = i + 1
            x_train, x_test = X[train_index], X[test_index]
            y_train, y_test = Y[train_index], Y[test_index]
            model = tf.keras.Sequential()
            model.add(Embedding(vocab_size, 128, weights=[embedding_matrix], input_length=X.shape[1],
                                trainable=True))
            model.add(SpatialDropout1D(0.25))
            model.add(LSTM(64, dropout=0.3))
            model.add(Dropout(0.2))
            kernel_regularizer = tf.keras.regularizers.L1L2()
            model.add(Dense(4, activation='softmax', kernel_regularizer=kernel_regularizer))
            optimizer = tf.keras.optimizers.Adam()
            model.compile(loss='categorical_crossentropy',
                          optimizer=optimizer, metrics=['accuracy'])
            print(model.summary())
            model.fit(x_train, y_train, epochs=100)
            accuracy_model.append(accuracy_score(y_test, np.round(
                model.predict(x_test)), normalize=True) * 100)
            f1_model.append(f1_score(y_test, np.round(
                model.predict(x_test)), average='weighted') * 100)
            recall_model.append(recall_score(y_test, np.round(
                model.predict(x_test)), average='weighted') * 100)
            precission_model.append(precision_score(y_test, np.round(
                model.predict(x_test)), average='weighted') * 100)
            model.save(os.path.join(self.path, "data", "fold", "model{}.h5").format(i))
            y_pred = model.predict_classes(x_test, batch_size=batch_size)
            df_test = pd.DataFrame({'true': y_test.tolist(), 'pred': y_pred})
            df_test['true'] = df_test['true'].apply(lambda x: np.argmax(x))
            print("confusion matrix", confusion_matrix(
                df_test.true, df_test.pred))
            df_test.to_csv(os.path.join(self.path, "data", "confusion", "confusion_matrix{}.csv").format(i))

        k=["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10"]
        average_accuracy = sum(accuracy_model) / len(accuracy_model)
        f1_average = sum(f1_model) / len(f1_model)
        precission_average = sum(precission_model) / len(precission_model)
        recall_average = sum(recall_model) / len(recall_model)
        df = pd.DataFrame({'Fold': k, 'Accuracy': accuracy_model, 'F1-Score': f1_model, 'Presisi': precission_model,
                           'Recall': recall_model})
        df.to_csv(os.path.join(self.path, "data", "fold", "kfold.csv"), index=False)
        print(f"Rata-rata akurasi sebesar {average_accuracy}")
        print(f"Rata-rata F1-Score sebesar {f1_average}")
        print(f"Rata-rata Precission sebesar {precission_average}")
        print(f"Rata-rata Recall sebesar {recall_average}")

    def new_model(self):
        self.tokenize_data()
        self.kfold_cross()
        self.load_model()

    def build_model(self):
        self.tokenize_data()
        # self.make_model()
        self.load_model()

    def predict_comment(self, text):
        model = load_model(self.basepath_model)
        with open(self.basepath_token, 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        komentar = [text]
        komentar = tokenizer2.texts_to_sequences(komentar)
        komentar = pad_sequences(komentar, maxlen=50, dtype='int32', value=0)
        sentiment = model.predict(komentar, batch_size=1, verbose=2)[0]
        return sentiment

    def cek_valid(self, array):
        global comment
        for i in range(len(array)):
            clear = self.normal.preprocessing(array[i])
            self.data_scrape.append(clear)
        with open(self.basepath_token, 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        comment = tokenizer2.texts_to_sequences(self.data_scrape)
        comment = pad_sequences(comment, maxlen=50, dtype='int32', value=0)
        validitas = []
        for x in comment:
            if x[-1] == 0:
                validitas.append("invalid")
            else:
                validitas.append("valid")
        return validitas
        
    def cek_validasi(self, array):
        with open(self.basepath_token, 'rb') as handle:
            tokenizer2 = pickle.load(handle)
        twt = [array]
        twt = tokenizer2.texts_to_sequences(twt)
        comment2 = pad_sequences(twt, maxlen=50, dtype='int32', value=0)
        x = comment2[0]
        print(x)
        if x[-1] == 0:
            return "invalid"
        else:
            return "valid"
        
    def prediction(self):
        model = load_model(self.basepath_model)
        return model.predict_classes(comment, batch_size=1)
